package structural

import "core:fmt"

// ============================================================================
// 1. COMPOSITE PATTERN
// ============================================================================
Graphic_Component :: struct {
    draw: proc(),
}

Dot_Leaf :: struct {
    using base: Graphic_Component,
    x: int,
    y: int,
}

dot_leaf_draw :: proc() {
    fmt.println("Drawing Dot Leaf")
}

Compound_Graphic_Composite :: struct {
    using base: Graphic_Component,
    children: [dynamic]^Graphic_Component,
}

compound_graphic_draw :: proc(self: ^Compound_Graphic_Composite) {
    for child in self.children {
        if child != nil && child.draw != nil {
            child.draw()
        }
    }
}

// ============================================================================
// 2. BRIDGE PATTERN
// ============================================================================
Storage_Engine_Driver :: struct {
    write_bytes: proc(path: string, data: []byte),
    read_bytes: proc(path: string) -> []byte,
}

Document_Repository :: struct {
    driver: ^Storage_Engine_Driver,
}

document_repository_save :: proc(self: ^Document_Repository, path: string, content: []byte) {
    if self.driver != nil && self.driver.write_bytes != nil {
        self.driver.write_bytes(path, content)
    }
}

// ============================================================================
// 3. ADAPTER PATTERN
// ============================================================================
Legacy_Printer :: struct {
    raw_print: proc(msg: cstring),
}

Modern_Printer_Interface :: struct {
    print_string: proc(msg: string),
}

Printer_Adapter :: struct {
    using base: Modern_Printer_Interface,
    adaptee: ^Legacy_Printer,
}

// ============================================================================
// 4. DECORATOR PATTERN
// ============================================================================
Notifier :: struct {
    send: proc(msg: string),
}

Logging_Notifier_Decorator :: struct {
    using base: Notifier,
    wrapped: ^Notifier,
}
