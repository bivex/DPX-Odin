"""Tests for ANTLR Odin Parser Adapter."""

from pattern_detector.adapters.outbound.antlr.odin_parser_adapter import OdinAntlrParserAdapter


def test_parse_package_and_structs() -> None:
    code = """
    package service

    import "core:fmt"
    import "core:os"

    User_Service :: struct {
        db_url: string,
    }

    user_service_instance: ^User_Service = nil

    user_service_process :: proc(self: ^User_Service, id: string) {
        fmt.println("Processing:", id)
    }
    """
    adapter = OdinAntlrParserAdapter()
    ns = adapter.parse_source(code, file_path="user_service.odin")

    assert ns.name == "service"
    assert len(ns.imports) == 2
    assert "User_Service" in ns.records
    rec = ns.records["User_Service"]
    assert "db_url" in rec.fields
    assert "user_service_instance" in ns.states
    assert ns.states["user_service_instance"].kind == "atom"
    assert ns.states["user_service_instance"].is_once is True
    assert "user_service_process" in ns.functions


def test_parse_interfaces_and_implementations() -> None:
    code = """
    package repo

    Crud_Repository :: struct {
        save: proc(entity: rawptr),
        find_by_id: proc(id: string) -> rawptr,
    }

    Database_Repository :: struct {
        using base: Crud_Repository,
        connection_string: string,
    }

    database_repository_save :: proc(self: ^Database_Repository, entity: rawptr) {}
    """
    adapter = OdinAntlrParserAdapter()
    ns = adapter.parse_source(code, file_path="database_repository.odin")

    assert "Crud_Repository" in ns.protocols
    proto = ns.protocols["Crud_Repository"]
    assert len(proto.methods) == 2
    assert proto.has_method("save")
    assert proto.has_method("find_by_id")

    assert "Database_Repository" in ns.records
    rec = ns.records["Database_Repository"]
    assert rec.implements_protocol("Crud_Repository")
