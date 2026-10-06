"""Type-Safe Bitmask Pattern Detection Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import PatternCategory, PatternType


class TypeSafeBitmaskRule(BasePatternRule):
    """Detects Type-Safe Bitmask Pattern (Odin bit_set idiom).

    Indicators:
    - Type definitions using `bit_set[Enum]` or `bit_set[Enum; UnderlyingType]`.
    - Eliminates unsafe raw bitwise integer shifts (&, |, <<) by introducing
      type-checked set operations (+, -, &, |, in) enforced by the Odin compiler.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TYPE_SAFE_BITMASK

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for rec in model.all_records():
            bit_set_spec = rec.field_types.get("bit_set")
            is_bit_set = "bit_set" in rec.implemented_protocols or bit_set_spec is not None

            if is_bit_set:
                spec_display = bit_set_spec or "bit_set"
                evidences = [
                    self.evidence(
                        description=f"Type '{rec.name}' is declared as a type-safe bitmask ({spec_display}), eliminating raw integer flag manipulation",
                        weight=0.70,
                        location=rec.location,
                        code_suffix="BIT_SET_TYPE_DECLARATION",
                    ),
                    self.evidence(
                        description="Replaces error-prone raw bitwise integer operations with compile-time checked set algebra (+, -, &, |, in)",
                        weight=0.25,
                        location=rec.location,
                        code_suffix="BIT_SET_TYPE_SAFETY",
                    ),
                ]

                detection = self.create_detection(
                    target_name=rec.name,
                    target_kind="bit_set_definition",
                    evidences=evidences,
                    primary_location=rec.location,
                    summary=f"Type-Safe Bitmask: '{rec.name}' encapsulates bit flags in type-checked {spec_display}",
                    base_score=0.35,
                )
                detection.pattern_category = PatternCategory.STRUCTURAL
                detections.append(detection)

        return detections
