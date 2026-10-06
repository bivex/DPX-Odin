"""Tests for design pattern rules on Odin source code."""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter
from pattern_detector.domain.rules.lifecycle_rule import LifecycleComponentPatternRule
from pattern_detector.domain.rules.singleton_rule import SingletonPatternRule
from pattern_detector.domain.rules.strategy_rule import StrategyPatternRule
from pattern_detector.domain.value_objects import PatternType


def test_strategy_pattern_odin() -> None:
    code = """
    package strategy

    Sort_Strategy :: struct {
        sort: proc(array: []int),
    }

    Quick_Sort :: struct {
        using base: Sort_Strategy,
    }

    quick_sort_sort :: proc(array: []int) {}

    Merge_Sort :: struct {
        using base: Sort_Strategy,
    }

    merge_sort_sort :: proc(array: []int) {}
    """
    model = OdinAntlrParserAdapter().parse_sources({"sort_strategy.odin": code})
    detections = StrategyPatternRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.STRATEGY
    assert detections[0].target_name == "Sort_Strategy"


def test_singleton_pattern_odin() -> None:
    code = """
    package singleton

    App_Config :: struct {
        port: int,
    }

    app_config_instance: ^App_Config = nil

    app_config_get_instance :: proc() -> ^App_Config {
        return app_config_instance
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"app_config.odin": code})
    detections = SingletonPatternRule().detect(model)
    assert len(detections) >= 1
    assert any(d.pattern_type == PatternType.SINGLETON for d in detections)


def test_lifecycle_component_pattern_odin() -> None:
    code = """
    package lifecycle

    Lifecycle :: struct {
        start: proc(),
        stop: proc(),
    }

    Http_Server_Component :: struct {
        using base: Lifecycle,
    }

    http_server_start :: proc() {}
    http_server_stop :: proc() {}
    """
    model = OdinAntlrParserAdapter().parse_sources({"lifecycle.odin": code})
    detections = LifecycleComponentPatternRule().detect(model)
    assert len(detections) >= 1
    assert any(d.pattern_type == PatternType.LIFECYCLE_COMPONENT for d in detections)
