"""Flyweight / Memoization & Object Cache Pattern Detection Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import PatternType


class FlyweightPatternRule(BasePatternRule):
    """Detects Flyweight / Memoization and Shared Object Cache pattern instances in Clojure.

    Indicators:
    - Usage of `memoize` to cache and share immutable computation results/objects.
    - Global definition binding holding a `memoize` wrapper over an expensive calculation.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FLYWEIGHT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. State / Var definitions using memoize
        for state in model.all_states():
            if state.initial_expr and "memoize" in state.initial_expr:
                evidences = [
                    self.evidence(
                        description=f"State '{state.name}' shares and caches fine-grained immutable instances using 'memoize'",
                        weight=0.70,
                        location=state.location,
                        code_suffix="MEMOIZE_CACHE",
                    ),
                ]
                detections.append(
                    self.create_detection(
                        target_name=state.name,
                        target_kind="memoized_flyweight_cache",
                        evidences=evidences,
                        primary_location=state.location,
                        related_locations=[],
                        summary=f"Flyweight pattern: '{state.name}' caches and shares immutable instances to eliminate redundant allocations",
                        base_score=0.25,
                    )
                )

        # 2. Functions calling memoize
        for fn in model.all_functions():
            if "memoize" in fn.calls or "clojure.core/memoize" in fn.calls:
                evidences = [
                    self.evidence(
                        description=f"Function '{fn.name}' employs 'memoize' caching to share fine-grained computed objects",
                        weight=0.65,
                        location=fn.location,
                        code_suffix="FN_MEMOIZE_USAGE",
                    ),
                ]
                detections.append(
                    self.create_detection(
                        target_name=fn.name,
                        target_kind="memoized_function",
                        evidences=evidences,
                        primary_location=fn.location,
                        related_locations=[],
                        summary=f"Flyweight pattern: function '{fn.name}' shares cached instances via memoization",
                        base_score=0.25,
                    )
                )

        # 3. Resource & Glyph Cache Flyweight (e.g. Font_Cache, Glyph_Cache, Texture_Pool)
        for rec in model.all_records():
            rec_name_lower = rec.name.lower()
            is_cache_name = any(
                k in rec_name_lower
                for k in ("cache", "pool", "atlas", "interner")
            )
            if is_cache_name and not rec.is_test:
                cache_methods = [
                    m.name
                    for m in rec.methods
                    if any(v in m.name.lower() for v in ("get", "lookup", "find", "place", "cache", "load", "intern", "fetch"))
                ]
                has_storage = any(
                    any(t in f_type.lower() for t in ("map[", "[dynamic]", "handle", "^", "table"))
                    for f_type in rec.field_types.values()
                ) or len(rec.fields) >= 2

                if has_storage or cache_methods:
                    evidences = [
                        self.evidence(
                            description=f"Record '{rec.name}' manages shared fine-grained instances/resources to prevent redundant allocations",
                            weight=0.55,
                            location=rec.location,
                            code_suffix="RESOURCE_CACHE_STORAGE",
                        )
                    ]
                    if cache_methods:
                        evidences.append(
                            self.evidence(
                                description=f"Provides flyweight retrieval/lookup operations: {', '.join(cache_methods[:4])}",
                                weight=0.35,
                                location=rec.location,
                                code_suffix="CACHE_LOOKUP_METHODS",
                            )
                        )
                    detections.append(
                        self.create_detection(
                            target_name=rec.name,
                            target_kind="flyweight_resource_cache",
                            evidences=evidences,
                            primary_location=rec.location,
                            related_locations=[],
                            summary=f"Flyweight pattern: '{rec.name}' caches and shares fine-grained instances",
                            base_score=0.25,
                        )
                    )

        return detections
