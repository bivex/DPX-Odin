"""Tests for Odin Package Dependency Graph and Circular Dependency Detection."""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter
from pattern_detector.domain.rules.circular_dependency_rule import CircularDependencyRule
from pattern_detector.domain.value_objects import PatternType


def test_circular_dependency_detection_odin() -> None:
    code_a = """
    package alpha

    import "beta"

    Alpha_Service :: struct {
        beta: ^beta.Beta_Service,
    }
    """
    code_b = """
    package beta

    import "alpha"

    Beta_Service :: struct {
        alpha: ^alpha.Alpha_Service,
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({
        "alpha.odin": code_a,
        "beta.odin": code_b,
    })

    cycles = model.find_circular_dependencies()
    assert len(cycles) == 1
    assert set(cycles[0]) == {"alpha", "beta"}

    rule = CircularDependencyRule()
    detections = rule.detect(model)
    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CIRCULAR_DEPENDENCY
    assert detections[0].confidence.score >= 0.80
