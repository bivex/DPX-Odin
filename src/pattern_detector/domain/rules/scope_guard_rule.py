"""Scope Guard (Defer Pattern) Detection Rule."""

from __future__ import annotations

import re

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import PatternCategory, PatternType

_DEFER_PATTERN = re.compile(r"\bdefer\s+([a-zA-Z_][a-zA-Z0-9_\.]*(?:\s*\([^\)]*\))?|\{[^\}]*\})")


class ScopeGuardRule(BasePatternRule):
    """Detects Scope Guard Pattern (Odin `defer` idiom).

    Indicators:
    - Procedures executing `defer <action>` to guarantee resource reclamation
      (closing handles, freeing buffers, unlocking mutexes) upon exiting the scope.
    - Eliminates resource leaks across multi-exit execution branches.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SCOPE_GUARD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for fn in model.all_functions():
            if not fn.body_text or fn.is_test:
                continue

            defer_matches = _DEFER_PATTERN.findall(fn.body_text)
            if not defer_matches:
                continue

            cleaned_defers = [d.strip() for d in defer_matches]
            sample_defers = ", ".join(cleaned_defers[:3])
            if len(cleaned_defers) > 3:
                sample_defers += f" (and {len(cleaned_defers) - 3} more)"

            evidences = [
                self.evidence(
                    description=(
                        f"Procedure '{fn.name}' employs Scope Guard pattern with {len(cleaned_defers)} "
                        f"deferred cleanup action(s): {sample_defers}"
                    ),
                    weight=0.60,
                    location=fn.location,
                    code_suffix="SCOPE_GUARD_DEFER",
                ),
                self.evidence(
                    description="Guarantees deterministic execution of resource cleanup actions on scope exit, preventing leaks",
                    weight=0.35,
                    location=fn.location,
                    code_suffix="SCOPE_GUARD_DETERMINISTIC_CLEANUP",
                ),
            ]

            detection = self.create_detection(
                target_name=fn.name,
                target_kind="scope_guard",
                evidences=evidences,
                primary_location=fn.location,
                summary=f"Scope Guard: '{fn.name}' defers cleanup operations ({sample_defers})",
                base_score=0.35,
            )
            detection.pattern_category = PatternCategory.BEHAVIORAL
            detections.append(detection)

        return detections
