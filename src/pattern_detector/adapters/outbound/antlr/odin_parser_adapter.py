"""Odin ANTLR4 Parser Adapter implementing ParserPort."""

from __future__ import annotations

import re
from typing import Any

from antlr4 import CommonTokenStream, InputStream

from pattern_detector.adapters.outbound.antlr.generated.odin.OdinLexer import OdinLexer
from pattern_detector.adapters.outbound.antlr.generated.odin.OdinParser import OdinParser
from pattern_detector.adapters.outbound.antlr.generated.odin.OdinParserVisitor import OdinParserVisitor
from pattern_detector.domain.code_model import (
    CodeModel,
    FunctionModel,
    MethodSignature,
    NamespaceModel,
    ProtocolExtensionModel,
    ProtocolModel,
    RecordModel,
    StateModel,
    WatchModel,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


class _OdinAstExtractionVisitor(OdinParserVisitor):
    """Walks the Odin parse tree to extract agnostic CodeModel domain entities."""

    def __init__(self, file_path: str, source_code: str) -> None:
        super().__init__()
        self.file_path = file_path
        self.source_code = source_code
        self.package_name = "main"
        self.requires: list[str] = []
        self.imports: list[str] = []
        self.protocols: dict[str, ProtocolModel] = {}
        self.records: dict[str, RecordModel] = {}
        self.functions: dict[str, FunctionModel] = {}
        self.states: dict[str, StateModel] = {}
        self.watches: list[WatchModel] = []
        self.extensions: list[ProtocolExtensionModel] = []

    def _get_location(self, ctx: Any) -> SourceLocation:
        if not ctx or not hasattr(ctx, "start") or not ctx.start:
            return SourceLocation(file_path=self.file_path, line=1, column=1)
        start = ctx.start
        stop = getattr(ctx, "stop", start) or start
        return SourceLocation(
            file_path=self.file_path,
            line=start.line,
            column=start.column + 1,
            end_line=stop.line,
            end_column=getattr(stop, "column", 0) + len(getattr(stop, "text", "") or "") + 1,
        )

    def _get_text(self, ctx: Any) -> str:
        if not ctx or not hasattr(ctx, "start") or not hasattr(ctx, "stop") or not ctx.start or not ctx.stop:
            return getattr(ctx, "getText", lambda: "")()
        start_idx = ctx.start.start
        stop_idx = ctx.stop.stop
        if start_idx is not None and stop_idx is not None and 0 <= start_idx <= stop_idx < len(self.source_code):
            return self.source_code[start_idx : stop_idx + 1]
        return ctx.getText()

    def visitPackageDecl(self, ctx: OdinParser.PackageDeclContext) -> Any:
        if ctx.qualifiedIdent():
            self.package_name = ctx.qualifiedIdent().getText()
        return self.visitChildren(ctx)

    def visitImportDecl(self, ctx: OdinParser.ImportDeclContext) -> Any:
        imp_path = ""
        if ctx.STRING_LIT():
            imp_path = ctx.STRING_LIT().getText().strip('"')
        elif ctx.RAW_STRING_LIT():
            imp_path = ctx.RAW_STRING_LIT().getText().strip("`")

        if imp_path:
            self.imports.append(imp_path)
            # Add package dependency for cross-module graph analysis
            clean_dep = imp_path.split("/")[-1].split(":")[-1]
            if clean_dep not in self.requires:
                self.requires.append(clean_dep)
            if imp_path not in self.requires:
                self.requires.append(imp_path)
        return self.visitChildren(ctx)

    def visitConstantDecl(self, ctx: OdinParser.ConstantDeclContext) -> Any:
        const_name = ctx.IDENT().getText() if ctx.IDENT() else ""
        loc = self._get_location(ctx)
        type_or_expr = ctx.typeOrExpr()
        if not type_or_expr or not const_name:
            return self.visitChildren(ctx)

        # 1. Struct Declaration
        if type_or_expr.structDecl():
            s_ctx = type_or_expr.structDecl()
            fields: list[str] = []
            field_types: dict[str, str] = {}
            implements_list: list[str] = []
            proc_pointer_signatures: list[MethodSignature] = []

            if s_ctx.structFieldList():
                for f_item in s_ctx.structFieldList().structField():
                    is_using = bool(f_item.USING())
                    f_type_str = f_item.type_().getText() if f_item.type_() else ""
                    f_loc = self._get_location(f_item)
                    if f_item.identList():
                        for id_tok in f_item.identList().IDENT():
                            f_name = id_tok.getText()

                            # Check if proc pointer signature
                            if f_item.type_() and f_item.type_().procType():
                                proc_pointer_signatures.append(
                                    MethodSignature(
                                        name=f_name,
                                        location=f_loc,
                                    )
                                )

                            # Subtyping / inheritance via `using` or base field
                            clean_base = f_type_str.lstrip("^[]")
                            if is_using or f_name in ("base", "super", "parent", "vtable"):
                                if clean_base and clean_base not in implements_list:
                                    implements_list.append(clean_base)
                            else:
                                fields.append(f_name)
                                if f_type_str:
                                    field_types[f_name] = f_type_str

            is_interface = bool(proc_pointer_signatures) or any(
                const_name.endswith(suffix)
                for suffix in (
                    "Interface",
                    "VTable",
                    "Strategy",
                    "Factory",
                    "Driver",
                    "Handler",
                    "Visitor",
                    "Command",
                    "Observer",
                    "Listener",
                    "Iterator",
                    "Lifecycle",
                    "Component",
                    "Broker",
                    "Calculator",
                )
            )

            # If struct defines proc pointers or acts as an interface/vtable, register as ProtocolModel
            if is_interface:
                self.protocols[const_name] = ProtocolModel(
                    name=const_name,
                    namespace=self.package_name,
                    location=loc,
                    methods=proc_pointer_signatures,
                    docstring="",
                    metadata={"is_interface": "true", "is_vtable": "true"},
                )

            self.records[const_name] = RecordModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                fields=fields,
                field_types=field_types,
                implemented_protocols=implements_list,
                methods=[],
                is_type=is_interface,
            )

        # 2. Union Declaration (Polymorphic Sum Type)
        elif type_or_expr.unionDecl():
            u_ctx = type_or_expr.unionDecl()
            variants: list[str] = []
            if u_ctx.typeList():
                for t in u_ctx.typeList().type_():
                    variants.append(t.getText())

            self.protocols[const_name] = ProtocolModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                methods=[],
                docstring="",
                metadata={"is_interface": "true", "is_union": "true", "variants": ",".join(variants)},
            )
            self.records[const_name] = RecordModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                fields=variants,
                implemented_protocols=[],
                is_type=True,
            )

        # 3. Procedure Declaration
        elif type_or_expr.procDecl():
            p_ctx = type_or_expr.procDecl()
            p_body = self._get_text(p_ctx.procBody()) if p_ctx.procBody() else ""
            param_names: list[str] = []
            param_types: list[str] = []
            first_param_type: str | None = None

            if p_ctx.paramList():
                for p_item in p_ctx.paramList().param():
                    t_str = p_item.type_().getText() if p_item.type_() else ""
                    if p_item.identList():
                        for id_tok in p_item.identList().IDENT():
                            param_names.append(id_tok.getText())
                            param_types.append(t_str)
                            if first_param_type is None:
                                first_param_type = t_str

            calls = set(re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s*\(", p_body))
            instantiates = set(re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s*\{", p_body))

            return_types_str = p_ctx.returnTypes().getText() if p_ctx.returnTypes() else ""
            raw_proc_text = self._get_text(p_ctx)
            doc_meta: list[str] = []
            if return_types_str:
                doc_meta.append(f"returns:{return_types_str}")
            if "#optional_ok" in raw_proc_text:
                doc_meta.append("optional_ok")
            if any("allocator" in p for p in param_names):
                doc_meta.append("explicit_allocator")

            fn_model = FunctionModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                parameter_lists=[param_names],
                body_text=p_body,
                calls=sorted(calls),
                instantiates_types=sorted(instantiates),
                docstring=";".join(doc_meta),
                is_private=False,
            )
            self.functions[const_name] = fn_model

            # Check if associated with a struct
            if first_param_type:
                receiver_type = first_param_type.lstrip("^")
                if receiver_type in self.records:
                    self.records[receiver_type].methods.append(fn_model)
                else:
                    for r_name, r_model in self.records.items():
                        if const_name.lower().startswith(r_name.lower() + "_"):
                            r_model.methods.append(fn_model)
                            break
            else:
                for r_name, r_model in self.records.items():
                    if const_name.lower().startswith(r_name.lower() + "_"):
                        r_model.methods.append(fn_model)
                        break

            # Observer subscriptions in procedure bodies: subscribe(broker, callback)
            watch_matches = re.findall(
                r"\b(?:subscribe|add_listener|add_observer|add_watch)\s*\(\s*([^,\)]+)\s*,\s*([^,\)]+)",
                p_body,
            )
            for target_obj, cb in watch_matches:
                t_clean = target_obj.strip("&^ ")
                cb_clean = cb.strip("&^ ")
                self.watches.append(
                    WatchModel(
                        target_state_name=t_clean,
                        watch_key="observer_listener",
                        callback_fn_name=cb_clean,
                        location=loc,
                    )
                )

        # 4. Compound Literal Instantiation (e.g. AUDIO_BACKEND_ALSA :: Audio_Backend_Interface { ... })
        elif (
            type_or_expr.expr()
            and hasattr(type_or_expr.expr(), "compoundLiteral")
            and type_or_expr.expr().compoundLiteral()
        ) or (hasattr(type_or_expr, "compoundLiteral") and type_or_expr.compoundLiteral()):
            lit = (
                type_or_expr.expr().compoundLiteral()
                if type_or_expr.expr() and hasattr(type_or_expr.expr(), "compoundLiteral") and type_or_expr.expr().compoundLiteral()
                else type_or_expr.compoundLiteral()
            )
            if lit and lit.type_():
                target_type = lit.type_().getText()
                lit_fields: list[str] = []
                lit_field_types: dict[str, str] = {}
                if lit.argumentList():
                    for arg in lit.argumentList().argument():
                        arg_name = arg.IDENT().getText() if arg.IDENT() else ""
                        arg_val = arg.expr().getText() if arg.expr() else (arg.type_().getText() if arg.type_() else "")
                        if arg_name:
                            lit_fields.append(arg_name)
                            if arg_val:
                                lit_field_types[arg_name] = arg_val

                self.records[const_name] = RecordModel(
                    name=const_name,
                    namespace=self.package_name,
                    location=loc,
                    fields=lit_fields,
                    field_types=lit_field_types,
                    implemented_protocols=[target_type],
                    methods=[],
                    is_type=False,
                )

        # 5. Distinct Type (e.g. Sound :: distinct Handle)
        elif type_or_expr.type_() and hasattr(type_or_expr.type_(), "distinctType") and type_or_expr.type_().distinctType():
            base_type = type_or_expr.type_().distinctType().type_().getText() if type_or_expr.type_().distinctType().type_() else ""
            self.records[const_name] = RecordModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                fields=[base_type] if base_type else [],
                field_types={"base_type": base_type} if base_type else {},
                implemented_protocols=[base_type] if base_type else [],
                methods=[],
                is_type=True,
            )

        # 6. Bit Set Declaration (e.g. Load_Texture_Options :: bit_set[Load_Texture_Option])
        elif (
            (hasattr(type_or_expr, "bitSetDecl") and type_or_expr.bitSetDecl())
            or (type_or_expr.type_() and hasattr(type_or_expr.type_(), "bitSetDecl") and type_or_expr.type_().bitSetDecl())
            or type_or_expr.getText().startswith("bit_set[")
        ):
            raw_text = type_or_expr.getText()
            self.records[const_name] = RecordModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                fields=[raw_text],
                field_types={"bit_set": raw_text},
                implemented_protocols=["bit_set"],
                methods=[],
                is_type=True,
            )

        # 7. Procedure Group (e.g. draw :: proc{draw_rect, draw_circle})
        elif hasattr(type_or_expr, "procGroup") and type_or_expr.procGroup():
            pg = type_or_expr.procGroup()
            overloads: list[str] = []
            if pg.exprList():
                for exp in pg.exprList().expr():
                    overloads.append(exp.getText())

            fn_model = FunctionModel(
                name=const_name,
                namespace=self.package_name,
                location=loc,
                parameter_lists=[],
                body_text=self._get_text(pg),
                calls=overloads,
                instantiates_types=[],
                docstring="procedure_group",
                is_private=False,
                is_multimethod=True,
                metadata={"overloads": ",".join(overloads)},
            )
            self.functions[const_name] = fn_model

        return self.visitChildren(ctx)

    def visitVariableDecl(self, ctx: OdinParser.VariableDeclContext) -> Any:
        # Crucial False Positive Protection: Only top-level variable declarations
        # can represent global singleton state in Odin. Local variables inside procedure bodies
        # or statement blocks must NEVER be extracted as global StateModels.
        if not isinstance(ctx.parentCtx, OdinParser.TopLevelDeclContext):
            return self.visitChildren(ctx)

        loc = self._get_location(ctx)
        if ctx.identList():
            var_names = [id_tok.getText() for id_tok in ctx.identList().IDENT()]
            for v_name in var_names:
                v_lower = v_name.lower()
                is_singleton = (
                    any(k in v_lower for k in ("instance", "singleton", "app_state", "app_context"))
                    or v_lower.endswith("_instance")
                    or v_lower.startswith("instance_")
                )
                if is_singleton:
                    self.states[v_name] = StateModel(
                        name=v_name,
                        namespace=self.package_name,
                        location=loc,
                        kind="atom",
                        is_once=True,
                        is_dynamic=True,
                    )
        return self.visitChildren(ctx)

    def finalize(self) -> None:
        """Post-processing resolution of struct protocol implementations."""
        for rec_name, rec in self.records.items():
            for proto_name in self.protocols:
                if rec_name == proto_name:
                    continue
                # If rec has a field with type of proto or pointer to proto
                for f_name, f_type in rec.field_types.items():
                    clean_type = re.sub(r"(\[dynamic\]|\[\d*\]|\[\?\]|\[\]|\^)", "", f_type).strip()
                    if (
                        clean_type == proto_name
                        and f_name in ("children", "items", "elements", "nodes", "members")
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)
                # If naming aligns with pattern interface (e.g. CreditCardStrategy -> PaymentStrategy)
                if not rec.is_type:
                    if (
                        proto_name.endswith("Strategy")
                        and rec_name.endswith("Strategy")
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)
                    if (
                        proto_name.endswith("Factory")
                        and rec_name.endswith("Factory")
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)
                    if (
                        proto_name.endswith("Component")
                        and rec_name.endswith(("Leaf", "Composite", "Component"))
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)
                    if (
                        proto_name.endswith("Calculator")
                        and rec_name.endswith("Calculator")
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)
                    if (
                        proto_name.endswith("Broker")
                        and rec_name.endswith("Broker")
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)
                    if (
                        proto_name.endswith("Lifecycle")
                        and rec_name.endswith("Component")
                        and proto_name not in rec.implemented_protocols
                    ):
                        rec.implemented_protocols.append(proto_name)

        # Link procedure references assigned in compound literal records to rec.methods
        for rec in self.records.values():
            for proc_name in rec.field_types.values():
                if proc_name in self.functions:
                    fn = self.functions[proc_name]
                    if fn not in rec.methods:
                        rec.methods.append(fn)

        # Link union variants defined in the same file into rec.implemented_protocols
        for proto_name, proto in self.protocols.items():
            if proto.metadata.get("is_union") == "true":
                raw_vars = proto.metadata.get("variants", "")
                variants = [v.strip().lstrip("^[]") for v in raw_vars.split(",") if v.strip()]
                for v in variants:
                    if v in self.records and proto_name not in self.records[v].implemented_protocols:
                        self.records[v].implemented_protocols.append(proto_name)


class OdinAntlrParserAdapter(ParserPort):
    """Parses Odin source files using ANTLR4 Odin grammar into agnostic CodeModel."""

    def parse_source(self, source_code: str, file_path: str = "") -> NamespaceModel:
        input_stream = InputStream(source_code)
        lexer = OdinLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = OdinParser(token_stream)

        tree = parser.compilationUnit()
        visitor = _OdinAstExtractionVisitor(file_path=file_path, source_code=source_code)
        visitor.visit(tree)
        visitor.finalize()

        return NamespaceModel(
            name=visitor.package_name,
            file_path=file_path,
            docstring="",
            requires=visitor.requires,
            imports=visitor.imports,
            protocols=visitor.protocols,
            records=visitor.records,
            extensions=visitor.extensions,
            functions=visitor.functions,
            states=visitor.states,
            watches=visitor.watches,
        )

    def parse_sources(self, sources: dict[str, str], max_workers: int | None = None) -> CodeModel:
        model = CodeModel()
        if not sources:
            return model

        if len(sources) > 3:
            import os
            from concurrent.futures import ThreadPoolExecutor

            workers = max_workers or min(16, (os.cpu_count() or 4) * 2)
            with ThreadPoolExecutor(max_workers=workers) as executor:
                namespaces = list(
                    executor.map(lambda item: self.parse_source(item[1], file_path=item[0]), sources.items())
                )
                for ns in namespaces:
                    model.add_namespace(ns)
        else:
            for file_path, source_code in sources.items():
                ns = self.parse_source(source_code, file_path=file_path)
                model.add_namespace(ns)

        return model
