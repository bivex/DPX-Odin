package creational

import "core:fmt"

// ============================================================================
// 1. SINGLETON PATTERN
// ============================================================================
Database_Connection_Pool :: struct {
    max_connections: int,
    connection_string: string,
}

database_connection_pool_instance: ^Database_Connection_Pool = nil

database_connection_pool_get_instance :: proc() -> ^Database_Connection_Pool {
    if database_connection_pool_instance == nil {
        database_connection_pool_instance = new(Database_Connection_Pool)
        database_connection_pool_instance.max_connections = 10
    }
    return database_connection_pool_instance
}

// ============================================================================
// 2. ABSTRACT FACTORY PATTERN
// ============================================================================
Button :: struct {
    render: proc(),
}

Checkbox :: struct {
    check: proc(),
}

GUI_Factory :: struct {
    create_button: proc() -> ^Button,
    create_checkbox: proc() -> ^Checkbox,
}

Windows_Button :: struct {
    using base: Button,
}

Windows_Checkbox :: struct {
    using base: Checkbox,
}

Windows_GUI_Factory :: struct {
    using base: GUI_Factory,
}

windows_gui_factory_create_button :: proc() -> ^Button {
    btn := new(Windows_Button)
    return auto_cast btn
}

windows_gui_factory_create_checkbox :: proc() -> ^Checkbox {
    chk := new(Windows_Checkbox)
    return auto_cast chk
}

// ============================================================================
// 3. BUILDER PATTERN
// ============================================================================
Server_Config :: struct {
    host: string,
    port: int,
    use_tls: bool,
}

Server_Builder :: struct {
    host: string,
    port: int,
    use_tls: bool,
}

server_builder_with_host :: proc(b: ^Server_Builder, host: string) -> ^Server_Builder {
    b.host = host
    return b
}

server_builder_with_port :: proc(b: ^Server_Builder, port: int) -> ^Server_Builder {
    b.port = port
    return b
}

server_builder_build :: proc(b: ^Server_Builder) -> Server_Config {
    return Server_Config{
        host = b.host,
        port = b.port,
        use_tls = b.use_tls,
    }
}
