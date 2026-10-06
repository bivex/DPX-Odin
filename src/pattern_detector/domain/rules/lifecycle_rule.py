"""Lifecycle Component Pattern Detection Rule."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType, SourceLocation

LIFECYCLE_PAIRS: tuple[tuple[str, str], ...] = (
    ("start", "stop"),
    ("init", "shutdown"),
    ("init", "destroy"),
    ("init", "deinit"),
    ("init", "cleanup"),
    ("init", "close"),
    ("init", "free"),
    ("open", "close"),
    ("acquire", "release"),
    ("load", "unload"),
)


class LifecycleComponentPatternRule(BasePatternRule):
    """Detects Lifecycle Component Pattern (Component / Integrant / Mount / Systems Lifecycle).

    Indicators:
    - Protocols or records implementing `Lifecycle` with paired lifecycle transitions (init/shutdown, start/stop).
    - Records implementing paired lifecycle methods or function pointer fields.
    - Component dependency maps or system builders.
    """

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.LIFECYCLE_COMPONENT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections: list[Detection] = []

        # 1. Protocols defining Lifecycle (start/stop, init/shutdown, etc.)
        for proto in model.all_protocols():
            method_names = {m.name.lower() for m in proto.methods}
            matched_pair = next(
                ((p_init, p_term) for p_init, p_term in LIFECYCLE_PAIRS if p_init in method_names and p_term in method_names),
                None,
            )
            if matched_pair or "lifecycle" in proto.name.lower():
                matched_methods = [m.name for m in proto.methods if m.name.lower() in (matched_pair or ())]
                pair_desc = f" ({', '.join(matched_methods)})" if matched_methods else ""
                proto_evidences = [
                    self.evidence(
                        description=f"Protocol '{proto.name}' defines explicit component lifecycle transitions{pair_desc}",
                        weight=0.60,
                        location=proto.location,
                        code_suffix="LIFECYCLE_PROTOCOL",
                    )
                ]
                detections.append(
                    self.create_detection(
                        target_name=proto.name,
                        target_kind="lifecycle_protocol",
                        evidences=proto_evidences,
                        primary_location=proto.location,
                        summary=f"Lifecycle pattern: protocol '{proto.name}' defines system lifecycle contract",
                        base_score=0.20,
                    )
                )

        # 2. Records implementing Lifecycle transitions
        for rec in model.all_records():
            evidences: list[Evidence] = []
            related_locs: list[SourceLocation] = []

            implements_lifecycle = any("lifecycle" in p.lower() for p in rec.implemented_protocols)

            rec_methods_lower = {m.name.lower() for m in rec.methods}
            rec_fields_lower = {f.lower() for f in rec.fields} | {k.lower() for k in rec.field_types}

            matched_pair = None
            for p_init, p_term in LIFECYCLE_PAIRS:
                has_init = (
                    p_init in rec_methods_lower
                    or p_init in rec_fields_lower
                    or any(m.endswith(f"_{p_init}") for m in rec_methods_lower)
                    or any(k.endswith(f"_{p_init}") for k in rec_fields_lower)
                )
                has_term = (
                    p_term in rec_methods_lower
                    or p_term in rec_fields_lower
                    or any(m.endswith(f"_{p_term}") for m in rec_methods_lower)
                    or any(k.endswith(f"_{p_term}") for k in rec_fields_lower)
                )
                if has_init and has_term:
                    matched_pair = (p_init, p_term)
                    break

            if implements_lifecycle:
                evidences.append(
                    self.evidence(
                        description=f"Record '{rec.name}' explicitly implements Lifecycle protocol",
                        weight=0.55,
                        location=rec.location,
                        code_suffix="IMPLEMENTS_LIFECYCLE",
                    )
                )

            if matched_pair:
                evidences.append(
                    self.evidence(
                        description=f"Record '{rec.name}' implements '{matched_pair[0]}' and '{matched_pair[1]}' lifecycle operations",
                        weight=0.65,
                        location=rec.location,
                        code_suffix="HAS_LIFECYCLE_METHODS",
                    )
                )

            if evidences and (implements_lifecycle or matched_pair):
                pair_name = f"{matched_pair[0]}/{matched_pair[1]}" if matched_pair else "lifecycle"
                detections.append(
                    self.create_detection(
                        target_name=rec.name,
                        target_kind="lifecycle_component",
                        evidences=evidences,
                        primary_location=rec.location,
                        related_locations=related_locs,
                        summary=f"Lifecycle Component pattern: stateful component '{rec.name}' with {pair_name} lifecycle",
                        base_score=0.15,
                    )
                )

        return detections
