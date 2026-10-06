package principles

import "core:fmt"

// ============================================================================
// 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP) & CLEAN CODE
// ============================================================================
Order_Receipt_Printer :: struct {
    formatter_name: string,
}

order_receipt_printer_print :: proc(self: ^Order_Receipt_Printer, order_id: string, amount: f64) {
    fmt.println("Receipt for order:", order_id, "amount:", amount)
}

Order_Repository :: struct {
    db_endpoint: string,
}

order_repository_save :: proc(self: ^Order_Repository, order_id: string) {
    fmt.println("Saved order to db:", order_id)
}

// ============================================================================
// 2. OPEN/CLOSED PRINCIPLE (OCP)
// ============================================================================
Tax_Calculator :: struct {
    calculate_tax: proc(amount: f64) -> f64,
}

Standard_Tax_Calculator :: struct {
    using base: Tax_Calculator,
}

standard_tax_calculate :: proc(amount: f64) -> f64 {
    return amount * 0.20
}

Reduced_Tax_Calculator :: struct {
    using base: Tax_Calculator,
}

reduced_tax_calculate :: proc(amount: f64) -> f64 {
    return amount * 0.07
}

Zero_Tax_Calculator :: struct {
    using base: Tax_Calculator,
}

zero_tax_calculate :: proc(amount: f64) -> f64 {
    return 0.0
}

// ============================================================================
// 3. INTERFACE SEGREGATION PRINCIPLE (ISP)
// ============================================================================
Printable :: struct {
    print: proc(),
}

Serializable_Entity :: struct {
    serialize: proc() -> string,
}

Invoice_Document :: struct {
    using printable: Printable,
    using serializable: Serializable_Entity,
}
