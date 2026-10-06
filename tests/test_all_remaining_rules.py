"""Tests for design pattern rules on Odin source code."""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter
from pattern_detector.domain.rules.abstract_factory_rule import AbstractFactoryRule
from pattern_detector.domain.rules.bridge_rule import BridgePatternRule
from pattern_detector.domain.rules.composite_rule import CompositePatternRule
from pattern_detector.domain.rules.iterator_rule import IteratorPatternRule
from pattern_detector.domain.rules.mediator_rule import MediatorPatternRule
from pattern_detector.domain.value_objects import PatternType


def test_abstract_factory_rule_odin() -> None:
    code = """
    package factory

    Button :: struct { render: proc() }
    Checkbox :: struct { check: proc() }

    GUI_Factory :: struct {
        create_button: proc() -> ^Button,
        create_checkbox: proc() -> ^Checkbox,
    }

    Win_Factory :: struct {
        using base: GUI_Factory,
    }

    Mac_Factory :: struct {
        using base: GUI_Factory,
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"gui_factory.odin": code})
    detections = AbstractFactoryRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.ABSTRACT_FACTORY
    assert detections[0].target_name == "GUI_Factory"


def test_composite_rule_odin() -> None:
    code = """
    package composite

    Graphic :: struct {
        draw: proc(),
    }

    Dot :: struct {
        using base: Graphic,
    }

    Compound_Graphic :: struct {
        using base: Graphic,
        children: [dynamic]^Graphic,
    }

    compound_graphic_draw :: proc(self: ^Compound_Graphic) {
        for g in self.children {
            if g != nil && g.draw != nil {
                g.draw()
            }
        }
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"graphic.odin": code})
    detections = CompositePatternRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.COMPOSITE
    assert detections[0].target_name == "Graphic"


def test_bridge_rule_odin() -> None:
    code = """
    package bridge

    Database_Driver :: struct {
        execute_query: proc(sql: string),
    }

    Database_Service :: struct {
        driver: ^Database_Driver,
    }

    database_service_run :: proc(self: ^Database_Service, sql: string) {
        if self.driver != nil && self.driver.execute_query != nil {
            self.driver.execute_query(sql)
        }
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"bridge.odin": code})
    detections = BridgePatternRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.BRIDGE


def test_iterator_rule_odin() -> None:
    code = """
    package iter

    Custom_Iterator :: struct {
        has_next: proc() -> bool,
        next: proc() -> rawptr,
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"custom_iterator.odin": code})
    detections = IteratorPatternRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.ITERATOR


def test_mediator_rule_odin() -> None:
    code = """
    package mediator

    Event_Broker :: struct {
        publish: proc(topic: string, msg: rawptr),
        subscribe: proc(topic: string, handler: rawptr),
    }

    Message_Hub :: struct {
        using base: Event_Broker,
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"mediator.odin": code})
    detections = MediatorPatternRule().detect(model)
    assert len(detections) >= 1
    assert any(d.pattern_type == PatternType.MEDIATOR for d in detections)
