"""Comprehensive False Positives Test Suite for DPX-Odin.

Verifies that ordinary, standard Odin idioms (data structs, math utilities,
collections, formatting, and helper procedures) do not produce false positive detections
for Design Patterns or SOLID Principle violations.
"""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter
from pattern_detector.domain.rules import get_default_rules
from pattern_detector.domain.services.pattern_detector import PatternDetectorService
from pattern_detector.domain.value_objects import ConfidenceLevel, PatternType


def _scan_snippet(code_map: dict[str, str]):
    adapter = OdinAntlrParserAdapter()
    model = adapter.parse_sources(code_map)
    detector = PatternDetectorService(rules=get_default_rules())
    return detector.detect_all(model)


def test_plain_pure_math_and_string_utilities_have_zero_detections() -> None:
    code = """
    package utils

    add :: proc(a: int, b: int) -> int {
        return a + b
    }

    multiply :: proc(x: int, y: int) -> int {
        return x * y
    }

    factorial :: proc(n: int) -> int {
        if n <= 1 {
            return 1
        }
        return n * factorial(n - 1)
    }
    """
    report = _scan_snippet({"math_utils.odin": code})
    assert report.total_detections_count == 0


def test_dto_struct_not_flagged_as_srp_god_object() -> None:
    code = """
    package dto

    Customer_Profile_Dto :: struct {
        id: string,
        first_name: string,
        last_name: string,
        email: string,
        phone_number: string,
        street_address: string,
        city: string,
        postal_code: string,
        country: string,
        status: string,
    }
    """
    report = _scan_snippet({"customer_dto.odin": code})
    srp_detections = [d for d in report.detections if d.pattern_type == PatternType.SINGLE_RESPONSIBILITY]
    assert len(srp_detections) == 0


def test_standard_equals_method_not_flagged_as_ocp_violation() -> None:
    code = """
    package domain

    Money_Value :: struct {
        amount: f64,
        currency: string,
    }

    money_equals :: proc(a: Money_Value, b: Money_Value) -> bool {
        return a.amount == b.amount && a.currency == b.currency
    }
    """
    report = _scan_snippet({"money_value.odin": code})
    ocp_detections = [d for d in report.detections if d.pattern_type == PatternType.OPEN_CLOSED]
    assert len(ocp_detections) == 0


def test_fluent_string_and_optional_chains_not_flagged_as_law_of_demeter() -> None:
    code = """
    package service

    import "core:strings"

    Data_Service :: struct {}

    data_service_format :: proc(s: string) -> string {
        return strings.to_upper(strings.trim_space(s))
    }
    """
    report = _scan_snippet({"data_service.odin": code})
    lod_detections = [d for d in report.detections if d.pattern_type == PatternType.LAW_OF_DEMETER]
    assert len(lod_detections) == 0


def test_service_instantiating_array_or_dto_not_flagged_as_dip_violation() -> None:
    code = """
    package service

    Item_Listing_Service :: struct {}

    item_listing_service_generate :: proc(self: ^Item_Listing_Service) -> [dynamic]string {
        res := make([dynamic]string)
        append(&res, "Item A")
        return res
    }
    """
    report = _scan_snippet({"item_listing_service.odin": code})
    dip_detections = [d for d in report.detections if d.pattern_type == PatternType.DEPENDENCY_INVERSION]
    assert len(dip_detections) == 0


def test_simple_record_getters_not_flagged_as_dry_duplicate_code() -> None:
    code_a = """
    package models

    User_Entity :: struct {
        id: string,
    }
    """
    code_b = """
    package models

    Product_Entity :: struct {
        id: string,
    }
    """
    report = _scan_snippet({
        "user_entity.odin": code_a,
        "product_entity.odin": code_b,
    })
    dry_detections = [d for d in report.detections if d.pattern_type == PatternType.DRY]
    assert len(dry_detections) == 0


def test_string_helpers_with_make_or_create_name_not_flagged_as_factory() -> None:
    code = """
    package helpers

    import "core:strings"

    make_uppercase :: proc(s: string) -> string {
        return strings.to_upper(s)
    }

    create_slug :: proc(title: string) -> string {
        return strings.to_lower(title)
    }
    """
    report = _scan_snippet({"string_helpers.odin": code})
    factory_detections = [
        d for d in report.detections
        if d.pattern_type == PatternType.FACTORY_METHOD and d.confidence.level in (ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH)
    ]
    assert len(factory_detections) == 0


def test_factory_and_observer_interfaces_not_falsely_flagged_as_strategy() -> None:
    code = """
    package patterns

    Widget :: struct {}

    Widget_Factory :: struct {
        create_widget: proc() -> ^Widget,
    }

    Simple_Widget_Factory :: struct {
        using base: Widget_Factory,
    }

    Event_Observer :: struct {
        on_event: proc(event: string),
    }

    User_Observer :: struct {
        using base: Event_Observer,
    }
    """
    report = _scan_snippet({"patterns.odin": code})
    strategy_detections = [d for d in report.detections if d.pattern_type == PatternType.STRATEGY]
    assert len(strategy_detections) == 0


def test_command_invoker_with_undo_not_flagged_as_memento() -> None:
    code = """
    package command

    Command_Invoker :: struct {
        history_count: int,
    }

    command_invoker_undo :: proc(self: ^Command_Invoker) {
        if self.history_count > 0 {
            self.history_count -= 1
        }
    }
    """
    report = _scan_snippet({"command_invoker.odin": code})
    memento_detections = [d for d in report.detections if d.pattern_type == PatternType.MEMENTO]
    assert len(memento_detections) == 0


def test_instanceof_in_tests_not_flagged_as_ocp_violation() -> None:
    code = """
    package test

    import "core:fmt"

    verify_creation :: proc(obj: rawptr) {
        if obj instanceof String {
            fmt.println("String")
        } else if obj instanceof Integer {
            fmt.println("Integer")
        }
    }
    """
    report = _scan_snippet({"sample_factory_test.odin": code})
    ocp_detections = [d for d in report.detections if d.pattern_type == PatternType.OPEN_CLOSED]
    assert len(ocp_detections) == 0


def test_controller_with_typed_fields_detected_for_dip() -> None:
    code = """
    package controller

    User_Repository :: struct {
        find_by_id: proc(id: int) -> rawptr,
    }

    User_Controller :: struct {
        users: ^User_Repository,
    }
    """
    report = _scan_snippet({"user_controller.odin": code})
    dip_detections = [d for d in report.detections if d.pattern_type == PatternType.DEPENDENCY_INVERSION]
    assert len(dip_detections) >= 1
    assert dip_detections[0].target_name == "User_Controller"


def test_local_variables_in_procedures_not_flagged_as_singletons() -> None:
    code = """
    package definition

    lookup :: proc(name: string) -> bool {
        global := globals[name] or_return
        local_global := get_local()
        cache := get_cache()
        pool := get_pool()
        return global != nil
    }
    """
    report = _scan_snippet({"definition.odin": code})
    singleton_detections = [d for d in report.detections if d.pattern_type == PatternType.SINGLETON]
    assert len(singleton_detections) == 0


def test_struct_with_pool_and_generic_types_not_flagged_as_singleton() -> None:
    code = """
    package nbio

    _IO :: struct {
        iocp: win.HANDLE,
        completed: queue.Queue(^Completion),
        completion_pool: Pool(Completion),
        io_pending: int,
    }
    """
    report = _scan_snippet({"nbio_internal.odin": code})
    singleton_detections = [d for d in report.detections if d.pattern_type == PatternType.SINGLETON]
    assert len(singleton_detections) == 0


def test_package_with_normal_imports_and_tests_not_flagged_as_tight_coupling() -> None:
    code = """
    package main

    import "core:fmt"
    import "src:server"
    import "server"
    import "src:common"
    """
    report = _scan_snippet({"tests/session_test.odin": code})
    coupling_detections = [d for d in report.detections if d.pattern_type == PatternType.HIGH_COHESION_LOW_COUPLING]
    assert len(coupling_detections) == 0
