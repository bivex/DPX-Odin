"""Procedure Group Pattern Detection Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import PatternCategory, PatternType


class ProcedureGroupRule(BasePatternRule):
    """Detects Procedure Group Pattern (Odin `proc{...}` static overload dispatcher).

    Indicators:
    - Procedures defined as procedure groups (`proc{fn1, fn2, ...}`).
    - Provides a unified API name resolved statically at compile-time by argument types,
      avoiding dynamic vtable lookups.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROCEDURE_GROUP

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            is_proc_group = fn.is_multimethod and (
                (fn.docstring and "procedure_group" in fn.docstring) or "overloads" in fn.metadata
            )
            if not is_proc_group:
                continue

            overloads_list = fn.calls
            overloads_desc = ", ".join(overloads_list) if overloads_list else "variants"

            evidences = [
                self.evidence(
                    description=(
                        f"Procedure Group '{fn.name}' aggregates {len(overloads_list)} concrete "
                        f"overload procedure(s) ({overloads_desc})"
                    ),
                    weight=0.65,
                    location=fn.location,
                    code_suffix="PROCEDURE_GROUP_OVERLOADS",
                ),
                self.evidence(
                    description=(
                        "Provides a unified polymorphic call site resolved statically at compile time "
                        "without runtime dispatch or vtable overhead"
                    ),
                    weight=0.30,
                    location=fn.location,
                    code_suffix="PROCEDURE_GROUP_STATIC_DISPATCH",
                ),
            ]

            detection = self.create_detection(
                target_name=fn.name,
                target_kind="procedure_group",
                evidences=evidences,
                primary_location=fn.location,
                summary=f"Procedure Group: '{fn.name}' statically dispatches over ({overloads_desc})",
                base_score=0.35,
            )
            detection.pattern_category = PatternCategory.BEHAVIORAL
            detections.append(detection)

        return detections
