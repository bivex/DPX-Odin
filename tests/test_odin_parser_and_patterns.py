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


def test_odin_compound_literal_interface_and_lifecycle() -> None:
    odin_code = """
    package audio

    Audio_Backend_Interface :: struct {
        init: proc() -> bool,
        shutdown: proc(),
    }

    alsa_init :: proc() -> bool { return true }
    alsa_shutdown :: proc() {}

    AUDIO_BACKEND_ALSA :: Audio_Backend_Interface {
        init = alsa_init,
        shutdown = alsa_shutdown,
    }

    AUDIO_BACKEND_WAVEOUT :: Audio_Backend_Interface {
        init = alsa_init,
        shutdown = alsa_shutdown,
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"audio.odin": odin_code})
    detector = PatternDetectorService(rules=get_default_rules())
    report = detector.detect_all(model)

    detected_types = {d.pattern_type for d in report.detections}
    assert PatternType.LIFECYCLE_COMPONENT in detected_types
    assert PatternType.STRATEGY in detected_types


def test_odin_tagged_union_command_and_visitor() -> None:
    odin_code = """
    package events

    Event :: union {
        Event_Key_Down,
        Event_Mouse_Move,
        Event_Close,
    }

    Event_Key_Down :: struct { key: int }
    Event_Mouse_Move :: struct { x: int, y: int }
    Event_Close :: struct {}

    dispatch_event :: proc(ev: Event) {
        switch e in ev {
        case Event_Key_Down:
        case Event_Mouse_Move:
        case Event_Close:
        }
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"events.odin": odin_code})
    detector = PatternDetectorService(rules=get_default_rules())
    report = detector.detect_all(model)

    detected_types = {d.pattern_type for d in report.detections}
    assert PatternType.COMMAND in detected_types
    assert PatternType.VISITOR in detected_types


def test_odin_handle_proxy_and_flyweight_cache() -> None:
    odin_code = """
    package res

    Handle :: distinct u64
    Texture_Handle :: distinct Handle
    Shader_Handle :: distinct Handle

    Texture_Cache :: struct {
        textures: map[string]Texture_Handle,
    }

    texture_cache_get :: proc(c: ^Texture_Cache, name: string) -> Texture_Handle {
        return c.textures[name]
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"res.odin": odin_code})
    detector = PatternDetectorService(rules=get_default_rules())
    report = detector.detect_all(model)

    detected_types = {d.pattern_type for d in report.detections}
    assert PatternType.PROXY in detected_types
    assert PatternType.FLYWEIGHT in detected_types


def test_odin_idioms_bitmask_and_procedure_group() -> None:
    odin_code = """
    package renderer

    Render_Flag :: enum {
        Wireframe,
        Depth_Test,
        Cull_Backface,
    }

    Render_Flags :: bit_set[Render_Flag]

    draw_rect :: proc(x, y, w, h: int) {}
    draw_circle :: proc(x, y, r: int) {}

    draw :: proc{draw_rect, draw_circle}
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"render.odin": odin_code})
    detector = PatternDetectorService(rules=get_default_rules())
    report = detector.detect_all(model)

    detected_types = {d.pattern_type for d in report.detections}
    assert PatternType.TYPE_SAFE_BITMASK in detected_types
    assert PatternType.PROCEDURE_GROUP in detected_types

    bitmask_det = next(d for d in report.detections if d.pattern_type == PatternType.TYPE_SAFE_BITMASK)
    assert bitmask_det.target_name == "Render_Flags"

    procgroup_det = next(d for d in report.detections if d.pattern_type == PatternType.PROCEDURE_GROUP)
    assert procgroup_det.target_name == "draw"


def test_odin_idioms_scope_guard_result_tuple_and_allocator_dip() -> None:
    odin_code = """
    package assets

    import "core:mem"

    Texture :: struct {
        id: u32,
    }

    load_texture :: proc(filename: string, allocator := context.allocator) -> (Texture, bool) #optional_ok {
        buf := make([]u8, 1024, allocator)
        defer delete(buf, allocator)

        return Texture{id = 1}, true
    }
    """

    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources({"assets.odin": odin_code})
    detector = PatternDetectorService(rules=get_default_rules())
    report = detector.detect_all(model)

    detected_types = {d.pattern_type for d in report.detections}
    assert PatternType.SCOPE_GUARD in detected_types
    assert PatternType.RESULT_TUPLE in detected_types
    assert PatternType.DEPENDENCY_INVERSION in detected_types

    guard_det = next(d for d in report.detections if d.pattern_type == PatternType.SCOPE_GUARD)
    assert guard_det.target_name == "load_texture"

    tuple_det = next(d for d in report.detections if d.pattern_type == PatternType.RESULT_TUPLE)
    assert tuple_det.target_name == "load_texture"

    dip_det = next(
        d
        for d in report.detections
        if d.pattern_type == PatternType.DEPENDENCY_INVERSION and d.target_kind == "dip_allocator_injection"
    )
    assert dip_det.target_name == "load_texture"
