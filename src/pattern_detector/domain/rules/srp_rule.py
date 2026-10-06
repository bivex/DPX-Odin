"""Single Responsibility Principle (SRP) Detection Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternCategory, PatternType, SourceLocation


class SingleResponsibilityRule(BasePatternRule):
    """Detects violations and adherences to the Single Responsibility Principle (SRP).

    Indicators:
    - God Object / Blob: Class with excessive methods (>10), high field count, and mixed concerns
      (e.g. database access + HTTP handling + JSON serialization + business computation).
    - Single-focus cohesive classes adhering strictly to SRP.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLE_RESPONSIBILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        concern_keywords = {
            "persistence": ("database", "repository", "dao", "sql", "persist", "query_db"),
            "http_web": ("http", "endpoint", "controller", "servlet", "webhook", "rest_api"),
            "serialization": ("json", "xml", "yaml", "serialize", "deserialize"),
            "auth_security": ("authenticate", "authorize", "token", "password", "crypto", "oauth", "jwt"),
            "business_logic": ("calculate", "compute", "process", "validate", "discount", "tax"),
        }

        for rec in model.all_records():
            if rec.name.endswith("Test") or rec.name.endswith("Tests"):
                continue

            # Exclude plain getters, setters, equals, hashCode, toString
            business_methods = [
                m
                for m in rec.methods
                if not m.name.split(".")[-1].startswith(("get", "set", "is", "has"))
                and m.name.split(".")[-1] not in ("equals", "hashcode", "tostring")
            ]
            method_names = [m.name.split(".")[-1].lower() for m in business_methods]
            fields_count = len(rec.fields)
            methods_count = len(business_methods)

            # Identify detected concern categories
            matched_concerns: dict[str, list[str]] = {}
            for concern, kws in concern_keywords.items():
                matching = [m for m in method_names if any(kw in m for kw in kws)]
                if matching:
                    matched_concerns[concern] = matching

            evidences: list[Evidence] = []

            # 1. God Object / Mixed Concerns Violation
            if len(matched_concerns) >= 3 or (methods_count >= 12 and len(matched_concerns) >= 2):
                concerns_str = ", ".join(f"{c} ({len(ms)} methods)" for c, ms in matched_concerns.items())
                evidences.append(
                    self.evidence(
                        description=f"Class '{rec.name}' mixes {len(matched_concerns)} disparate concerns ({concerns_str}), violating SRP",
                        weight=min(0.60, 0.30 + 0.10 * len(matched_concerns)),
                        location=rec.location,
                        code_suffix="SRP_MIXED_CONCERNS",
                    )
                )

                if methods_count >= 10:
                    evidences.append(
                        self.evidence(
                            description=f"High method count ({methods_count} methods) indicates bloated class responsibility",
                            weight=min(0.40, 0.20 + 0.02 * methods_count),
                            location=rec.location,
                            code_suffix="SRP_HIGH_METHOD_COUNT",
                        )
                    )

                if fields_count >= 6:
                    evidences.append(
                        self.evidence(
                            description=f"High field count ({fields_count} fields) suggests multi-purpose state holder",
                            weight=0.25,
                            location=rec.location,
                            code_suffix="SRP_HIGH_FIELD_COUNT",
                        )
                    )

                detections.append(
                    self.create_detection(
                        target_name=rec.name,
                        target_kind="god_class_srp_violation",
                        evidences=evidences,
                        primary_location=rec.location,
                        summary=f"SRP Violation (God Class): '{rec.name}' mixes {len(matched_concerns)} concerns across {methods_count} methods",
                        base_score=0.40,
                    )
                )
                # Assign PRINCIPLE category
                detections[-1].pattern_category = PatternCategory.PRINCIPLE

        # 2. God Module / God File (Files with >35 functions violating modular SRP)
        for ns in model.namespaces.values():
            fn_count = len(ns.functions)
            if fn_count >= 35:
                file_name = ns.file_path.split("/")[-1]
                evidences = [
                    self.evidence(
                        description=f"File/module '{file_name}' defines {fn_count} procedures in a single file, violating SRP",
                        weight=min(0.65, 0.35 + 0.005 * fn_count),
                        location=SourceLocation(file_path=ns.file_path, line=1),
                        code_suffix="SRP_GOD_MODULE",
                    ),
                    self.evidence(
                        description="Monolithic module file should be decomposed into dedicated cohesive subpackages",
                        weight=0.30,
                        location=SourceLocation(file_path=ns.file_path, line=1),
                        code_suffix="SRP_MODULAR_DECOMPOSITION_NEEDED",
                    ),
                ]
                detection = self.create_detection(
                    target_name=file_name,
                    target_kind="god_module_srp_violation",
                    evidences=evidences,
                    primary_location=SourceLocation(file_path=ns.file_path, line=1),
                    summary=f"SRP Violation (God Module): '{file_name}' aggregates {fn_count} procedures in a single monolithic file",
                    base_score=0.35,
                )
                detection.pattern_category = PatternCategory.PRINCIPLE
                detections.append(detection)

        return detections
