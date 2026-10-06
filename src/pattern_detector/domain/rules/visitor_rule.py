"""Visitor Pattern Detection Rule."""

from __future__ import annotations

import re

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternCategory, PatternType, SourceLocation


class VisitorPatternRule(BasePatternRule):
    """Detects Visitor pattern instances in Java.

    Indicators:
    - Visitor Interface: An interface declaring overloaded `visit(...)` methods for different element types.
    - Element Interface / Classes: Interfaces declaring `accept(Visitor v)` and classes invoking `visitor.visit(this)`.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.VISITOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Visitor Interfaces declaring visit(...) methods
        for proto in model.all_protocols():
            if proto.location.is_test_location or proto.name.endswith(("Test", "Tests", "TestCase")):
                continue
            visit_methods = [m for m in proto.methods if "visit" in m.name.lower()]
            if visit_methods and ("visitor" in proto.name.lower() or len(visit_methods) >= 2):
                evidences: list[Evidence] = [
                    self.evidence(
                        description=f"Interface '{proto.name}' defines Visitor contract with {len(visit_methods)} visit() method overload(s)",
                        weight=min(0.65, 0.40 + 0.08 * len(visit_methods)),
                        location=proto.location,
                        code_suffix="VISITOR_INTERFACE_METHODS",
                    )
                ]

                # Check concrete visitor implementations
                visitor_impls = [r for r in model.find_records_implementing(proto.name) if not r.is_test]
                related_locs: list[SourceLocation] = []
                if visitor_impls:
                    impl_names = ", ".join(r.name for r in visitor_impls[:4])
                    evidences.append(
                        self.evidence(
                            description=f"Concrete visitor classes implemented: {impl_names}",
                            weight=0.30,
                            location=visitor_impls[0].location,
                            code_suffix="CONCRETE_VISITOR_IMPLEMENTATIONS",
                        )
                    )
                    related_locs.extend(r.location for r in visitor_impls)

                detection = self.create_detection(
                    target_name=proto.name,
                    target_kind="visitor_interface",
                    evidences=evidences,
                    primary_location=proto.location,
                    related_locations=related_locs,
                    summary=f"Visitor pattern: '{proto.name}' defines double-dispatch visitor operations over element hierarchy",
                    base_score=0.35,
                )
                detection.pattern_category = PatternCategory.BEHAVIORAL
                detections.append(detection)

        # 2. Element Accept Methods calling visit(this)
        for rec in model.all_records():
            if rec.is_test:
                continue
            accept_methods = [m for m in rec.methods if "accept" in m.name.lower()]
            for am in accept_methods:
                body = am.body_text or ""
                if "visit(" in body or ".visit" in body:
                    evidences = [
                        self.evidence(
                            description=f"Class '{rec.name}' implements double-dispatch accept() method delegating to visitor.visit(this)",
                            weight=0.65,
                            location=am.location,
                            code_suffix="ELEMENT_ACCEPT_DOUBLE_DISPATCH",
                        )
                    ]
                    detection = self.create_detection(
                        target_name=f"{rec.name}.{am.name.split('.')[-1]}",
                        target_kind="element_accept_method",
                        evidences=evidences,
                        primary_location=am.location,
                        summary=f"Visitor Element: '{rec.name}' participates in visitor double-dispatch via accept()",
                        base_score=0.35,
                    )
                    detection.pattern_category = PatternCategory.BEHAVIORAL
                    detections.append(detection)

        # 3. Type-Switch Visitor (Odin/Data-Oriented type inspection over unions)
        for fn in model.all_functions():
            if fn.location.is_test_location or fn.is_test:
                continue
            body = fn.body_text or ""
            switch_in_matches = re.findall(
                r"(?:#partial\s+)?switch\s+(?:&)?([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+([a-zA-Z_][a-zA-Z0-9_\.]*)",
                body,
            )
            case_matches = re.findall(r"\bcase\s+([a-zA-Z_][a-zA-Z0-9_]+)\s*:", body)
            if switch_in_matches and len(case_matches) >= 3:
                _, target_expr = switch_in_matches[0]
                evidences = [
                    self.evidence(
                        description=f"Procedure '{fn.name}' performs exhaustive type inspection over '{target_expr}' across {len(case_matches)} cases: {', '.join(case_matches[:5])}",
                        weight=min(0.65, 0.40 + 0.05 * len(case_matches)),
                        location=fn.location,
                        code_suffix="TYPE_SWITCH_VISITOR_DISPATCH",
                    ),
                    self.evidence(
                        description="Data-oriented Visitor pattern: separates operations from polymorphic union data structures",
                        weight=0.30,
                        location=fn.location,
                        code_suffix="TYPE_SAFE_VISITOR",
                    ),
                ]
                detection = self.create_detection(
                    target_name=fn.name,
                    target_kind="type_switch_visitor",
                    evidences=evidences,
                    primary_location=fn.location,
                    summary=f"Visitor pattern: procedure '{fn.name}' dispatches operations over {len(case_matches)} types of '{target_expr}'",
                    base_score=0.30,
                )
                detection.pattern_category = PatternCategory.BEHAVIORAL
                detections.append(detection)

        return detections
