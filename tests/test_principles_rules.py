"""Unit tests for SOLID Principles, Clean Code, Coupling & Cohesion Rules on Odin."""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter
from pattern_detector.domain.rules.cohesion_coupling_rule import CohesionCouplingRule
from pattern_detector.domain.rules.composition_over_inheritance_rule import CompositionOverInheritanceRule
from pattern_detector.domain.rules.dip_rule import DependencyInversionRule
from pattern_detector.domain.rules.dry_rule import DryRule
from pattern_detector.domain.rules.isp_rule import InterfaceSegregationRule
from pattern_detector.domain.rules.kiss_rule import KissRule
from pattern_detector.domain.rules.law_of_demeter_rule import LawOfDemeterRule
from pattern_detector.domain.rules.lsp_rule import LiskovSubstitutionRule
from pattern_detector.domain.rules.ocp_rule import OpenClosedPrincipleRule
from pattern_detector.domain.rules.srp_rule import SingleResponsibilityRule
from pattern_detector.domain.value_objects import PatternCategory, PatternType


def test_srp_god_object_violation() -> None:
    code = """
    package service

    Mega_God_Manager :: struct {
        db_url: string,
        http_port: string,
        jwt_secret: string,
        cache_host: string,
        retry_count: int,
        is_dev: bool,
        log_file: string,
        metric_name: string,
        cluster_id: string,
        queue_name: string,
        topic_name: string,
    }

    mega_save_to_database :: proc(self: ^Mega_God_Manager) {}
    mega_delete_from_database :: proc(self: ^Mega_God_Manager) {}
    mega_query_database :: proc(self: ^Mega_God_Manager) {}
    mega_handle_http_request :: proc(self: ^Mega_God_Manager) {}
    mega_get_http_endpoint :: proc(self: ^Mega_God_Manager) {}
    mega_serialize_to_json :: proc(self: ^Mega_God_Manager) {}
    mega_parse_xml :: proc(self: ^Mega_God_Manager) {}
    mega_authenticate_user :: proc(self: ^Mega_God_Manager) {}
    mega_calculate_taxes :: proc(self: ^Mega_God_Manager) {}
    mega_compute_discounts :: proc(self: ^Mega_God_Manager) {}
    mega_process_order :: proc(self: ^Mega_God_Manager) {}
    mega_validate_payment :: proc(self: ^Mega_God_Manager) {}
    """
    model = OdinAntlrParserAdapter().parse_sources({"mega_god_manager.odin": code})
    detections = SingleResponsibilityRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.SINGLE_RESPONSIBILITY
    assert detections[0].pattern_category == PatternCategory.PRINCIPLE


def test_ocp_instanceof_cascade_violation() -> None:
    code = """
    package graphics

    import "core:fmt"

    Shape_Drawer :: struct {}

    shape_drawer_draw :: proc(self: ^Shape_Drawer, shape: rawptr) {
        if shape instanceof Circle {
            fmt.println("Drawing circle")
        } else if shape instanceof Square {
            fmt.println("Drawing square")
        } else if shape instanceof Triangle {
            fmt.println("Drawing triangle")
        }
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"shape_drawer.odin": code})
    detections = OpenClosedPrincipleRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.OPEN_CLOSED
    assert "instanceof" in detections[0].evidences[0].description


def test_lsp_unsupported_operation_violation() -> None:
    code = """
    package collections

    Read_Only_List :: struct {
        get: proc(index: int),
        add: proc(item: rawptr),
    }

    Immutable_List_Impl :: struct {
        using base: Read_Only_List,
    }

    immutable_list_add :: proc(self: ^Immutable_List_Impl, item: rawptr) {
        panic("UnsupportedOperationException: Immutable list cannot be modified")
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"immutable_list.odin": code})
    detections = LiskovSubstitutionRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.LISKOV_SUBSTITUTION


def test_isp_fat_interface_violation() -> None:
    code = """
    package worker

    Monolithic_Worker :: struct {
        code: proc(),
        test: proc(),
        deploy: proc(),
        manage_infrastructure: proc(),
        review_budget: proc(),
        design_graphics: proc(),
        recruit_employees: proc(),
        handle_customer_support: proc(),
        clean_office: proc(),
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"monolithic_worker.odin": code})
    detections = InterfaceSegregationRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.INTERFACE_SEGREGATION


def test_dip_concrete_instantiation_violation() -> None:
    code = """
    package service

    Order_Processing_Service :: struct {}

    order_processing_service_process :: proc(self: ^Order_Processing_Service) {
        repo := new MySqlDatabaseRepository()
        repo.save()
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"order_processing_service.odin": code})
    detections = DependencyInversionRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.DEPENDENCY_INVERSION


def test_composition_over_inheritance_deep_hierarchy() -> None:
    code = """
    package hierarchy

    Base_Entity :: struct {}
    Auditable_Entity :: struct { using base: Base_Entity }
    Versioned_Entity :: struct { using base: Auditable_Entity }
    Concrete_User_Entity :: struct { using base: Versioned_Entity }
    """
    model = OdinAntlrParserAdapter().parse_sources({"hierarchy.odin": code})
    detections = CompositionOverInheritanceRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.COMPOSITION_OVER_INHERITANCE


def test_law_of_demeter_train_wreck_violation() -> None:
    code = """
    package shipping

    import "core:fmt"

    Shipping_Service :: struct {}

    shipping_service_calculate :: proc(self: ^Shipping_Service, order: ^Order) {
        zip := order.getCustomer().getAddress().getLocation().getPostalCode()
        fmt.println("Zip:", zip)
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"shipping_service.odin": code})
    detections = LawOfDemeterRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.LAW_OF_DEMETER


def test_kiss_long_parameter_list_violation() -> None:
    code = """
    package complex

    import "core:fmt"

    Complex_Calculator :: struct {}

    complex_calculator_compute :: proc(self: ^Complex_Calculator, a: int, b: int, name: string, rate: f64, flag: bool, mode: string, ctx: rawptr) {
        fmt.println("Computing")
    }
    """
    model = OdinAntlrParserAdapter().parse_sources({"complex_calculator.odin": code})
    detections = KissRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.KISS


def test_dry_duplicate_code_violation() -> None:
    code_a = """
    package dups

    Alpha_Processor :: struct {}

    alpha_processor_calculate :: proc(self: ^Alpha_Processor, price: f64, count: int) -> f64 {
        base := price * count
        if base > 100.0 {
            return base * 0.85
        }
        return base * 0.95
    }
    """
    code_b = """
    package dups

    Beta_Processor :: struct {}

    beta_processor_compute :: proc(self: ^Beta_Processor, price: f64, count: int) -> f64 {
        base := price * count
        if base > 100.0 {
            return base * 0.85
        }
        return base * 0.95
    }
    """
    model = OdinAntlrParserAdapter().parse_sources(
        {
            "alpha_processor.odin": code_a,
            "beta_processor.odin": code_b,
        }
    )
    detections = DryRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.DRY


def test_cohesion_coupling_high_fan_out() -> None:
    code_hub = """
    package hub

    import "mod1"
    import "mod2"
    import "mod3"
    import "mod4"

    Global_Orchestrator :: struct {}
    """
    model = OdinAntlrParserAdapter().parse_sources(
        {
            "global_orchestrator.odin": code_hub,
            "mod1.odin": "package mod1\nMod1 :: struct {}",
            "mod2.odin": "package mod2\nMod2 :: struct {}",
            "mod3.odin": "package mod3\nMod3 :: struct {}",
            "mod4.odin": "package mod4\nMod4 :: struct {}",
        }
    )
    detections = CohesionCouplingRule().detect(model)
    assert len(detections) >= 1
    assert detections[0].pattern_type == PatternType.HIGH_COHESION_LOW_COUPLING
