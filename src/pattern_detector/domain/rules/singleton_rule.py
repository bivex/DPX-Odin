"""Singleton Pattern Detection Rule for Odin."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation


class SingletonPatternRule(BasePatternRule):
    """Detects Singleton Pattern instances in Odin.

    Indicators:
    - Global pointer declaration (e.g. `instance: ^Config = nil`).
    - Dedicated getter/initializer procedure (e.g. `get_instance`).
    - Single shared instance lifecycle in package scope.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLETON

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        for state in model.all_states():
            evidences: list[Evidence] = []
            related_locs: list[SourceLocation] = []

            if state.is_once:
                evidences.append(
                    self.evidence(
                        description=f"Package-level singleton definition for '{state.name}' ensuring single-instance lifecycle",
                        weight=0.60,
                        location=state.location,
                        code_suffix="DEFONCE_DECLARATION",
                    )
                )

            if state.kind in ("pointer", "atom", "ref", "agent"):
                evidences.append(
                    self.evidence(
                        description=f"Holds stateful pointer container ({state.kind}) for global singleton state",
                        weight=0.35,
                        location=state.location,
                        code_suffix="STATEFUL_CONTAINER",
                    )
                )

            # Check if there are dedicated getter/setter functions in the same namespace accessing this state
            ns = model.get_namespace(state.namespace)
            if ns:
                accessors = [
                    f for f in ns.functions.values()
                    if state.name in f.calls or state.name in f.body_text or f.name.lower().endswith("instance")
                ]
                if accessors:
                    evidences.append(
                        self.evidence(
                            description=f"Has {len(accessors)} dedicated accessor/management functions: {', '.join(a.name for a in accessors[:3])}",
                            weight=0.25,
                            location=accessors[0].location,
                            code_suffix="ACCESSOR_FUNCTIONS",
                        )
                    )
                    for a in accessors:
                        related_locs.append(a.location)

            # Check singleton naming hints
            name_lower = state.name.lower()
            if any(hint in name_lower for hint in ("instance", "singleton", "app_state", "app_context")):
                evidences.append(
                    self.evidence(
                        description=f"Name '{state.name}' suggests shared singleton entity",
                        weight=0.20,
                        location=state.location,
                        code_suffix="SINGLETON_NAMING",
                    )
                )

            if state.is_once or (state.kind in ("pointer", "atom", "ref") and len(evidences) >= 2):
                detections.append(
                    self.create_detection(
                        target_name=state.name,
                        target_kind="singleton_state",
                        evidences=evidences,
                        primary_location=state.location,
                        related_locations=related_locs,
                        summary=f"Singleton pattern: global state container '{state.name}' with managed lifecycle",
                        base_score=0.15 if state.is_once else 0.05,
                    )
                )

        return detections
