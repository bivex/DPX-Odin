"""Tests for Odin ANTLR4 Parser Adapter and Odin Pattern Detection."""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter
from pattern_detector.domain.rules import get_default_rules
from pattern_detector.domain.services.pattern_detector import PatternDetectorService
from pattern_detector.domain.value_objects import PatternType


def test_odin_parser_extracts_structs_and_interfaces() -> None:
    odin_code = """
    package service

    import "core:fmt"

    Order_Processor :: struct {
        process_order: proc(order_id: int),
        validate: proc(customer_id: string) -> bool,
    }

    Standard_Order_Processor :: struct {
        using base: Order_Processor,
        endpoint: string,
    }

    standard_order_processor_process :: proc(self: ^Standard_Order_Processor, order_id: int) {
        fmt.println("Processing order:", order_id)
    }

    standard_order_processor_validate :: proc(self: ^Standard_Order_Processor, customer_id: string) -> bool {
        return customer_id != ""
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"order_processor.odin": odin_code})

    assert "service" in model.namespaces
    ns = model.namespaces["service"]
    assert "Order_Processor" in ns.protocols
    assert len(ns.protocols["Order_Processor"].methods) == 2
    assert "Standard_Order_Processor" in ns.records
    assert "Order_Processor" in ns.records["Standard_Order_Processor"].implemented_protocols


def test_odin_pattern_detection_strategy_and_composite() -> None:
    odin_code = """
    package design

    import "core:fmt"

    Graphic :: struct {
        render: proc(),
    }

    Circle :: struct {
        using base: Graphic,
    }

    circle_render :: proc() {
        fmt.println("Circle")
    }

    Canvas_Container :: struct {
        using base: Graphic,
        children: [dynamic]^Graphic,
    }

    canvas_container_render :: proc(self: ^Canvas_Container) {
        for g in self.children {
            if g != nil && g.render != nil {
                g.render()
            }
        }
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"graphic.odin": odin_code})
    detector = PatternDetectorService(rules=get_default_rules())
    report = detector.detect_all(model)

    assert report.total_detections_count >= 1
    pattern_types = [d.pattern_type for d in report.detections]
    assert PatternType.STRATEGY in pattern_types or PatternType.COMPOSITE in pattern_types
