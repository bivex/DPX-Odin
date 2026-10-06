"""Result Tuple Error Handling Pattern Detection Rule."""

from __future__ import annotations

import re

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import PatternCategory, PatternType

_RESULT_TUPLE_RETURNS_RE = re.compile(
    r"returns:\((?:[^,\)]+,\s*)*(?:[a-zA-Z0-9_]*:)?\s*(?:bool|error|err|result_code|status)\s*,?\)",
    re.IGNORECASE,
)


class ResultTupleRule(BasePatternRule):
    """Detects Result Tuple Error Handling Pattern (Odin `(val, ok)` / `#optional_ok` idiom).

    Indicators:
    - Procedures returning multiple values where the final value is a status/boolean
      flag or explicit error (e.g. `(T, bool)`, `(T, Error)`).
    - Procedures tagged with the `#optional_ok` directive allowing optional discarding
      of the boolean status code.
    - Eliminates exception overhead and unhandled crashes via explicit compile-time typing.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.RESULT_TUPLE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if fn.is_test:
                continue

            doc = fn.docstring or ""
            returns_match = re.search(r"returns:([^\;]+)", doc)
            returns_snippet = returns_match.group(1).strip() if returns_match else ""

            # A result tuple must return multiple values in parentheses
            is_tuple = returns_snippet.startswith("(") and returns_snippet.endswith(")") and "," in returns_snippet
            if not is_tuple:
                continue

            has_optional_ok = "optional_ok" in doc
            has_result_tuple = bool(_RESULT_TUPLE_RETURNS_RE.search(doc))

            if not (has_optional_ok or has_result_tuple):
                continue

            evidences = [
                self.evidence(
                    description=f"Procedure '{fn.name}' returns explicit result tuple {returns_snippet} for error signaling",
                    weight=0.60,
                    location=fn.location,
                    code_suffix="RESULT_TUPLE_RETURN_SIGNATURE",
                )
            ]

            if has_optional_ok:
                evidences.append(
                    self.evidence(
                        description=(
                            f"Procedure '{fn.name}' is annotated with '#optional_ok', enabling idiomatic "
                            f"Odin unpack syntax `val, ok := {fn.name}(...)` or direct single-value consumption"
                        ),
                        weight=0.35,
                        location=fn.location,
                        code_suffix="RESULT_TUPLE_OPTIONAL_OK_TAG",
                    )
                )
            else:
                evidences.append(
                    self.evidence(
                        description="Enforces explicit, zero-overhead error checking at call sites without exceptions",
                        weight=0.35,
                        location=fn.location,
                        code_suffix="RESULT_TUPLE_EXPLICIT_HANDLING",
                    )
                )

            summary_extra = " with #optional_ok" if has_optional_ok else ""
            detection = self.create_detection(
                target_name=fn.name,
                target_kind="result_tuple_procedure",
                evidences=evidences,
                primary_location=fn.location,
                summary=f"Result Tuple: '{fn.name}' returns {returns_snippet}{summary_extra}",
                base_score=0.35,
            )
            detection.pattern_category = PatternCategory.PRINCIPLE
            detections.append(detection)

        return detections
