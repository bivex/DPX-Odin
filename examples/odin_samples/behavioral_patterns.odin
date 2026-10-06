package behavioral

import "core:fmt"

// ============================================================================
// 1. STRATEGY PATTERN
// ============================================================================
Payment_Strategy :: struct {
    pay: proc(amount: int),
}

Credit_Card_Strategy :: struct {
    using base: Payment_Strategy,
    card_number: string,
}

credit_card_pay :: proc(amount: int) {
    fmt.println("Paid via Credit Card:", amount)
}

Crypto_Strategy :: struct {
    using base: Payment_Strategy,
    wallet_address: string,
}

crypto_pay :: proc(amount: int) {
    fmt.println("Paid via Crypto:", amount)
}

// ============================================================================
// 2. MEDIATOR PATTERN
// ============================================================================
Event_Broker :: struct {
    publish: proc(topic: string, event: rawptr),
    subscribe: proc(topic: string, handler: rawptr),
}

Central_Message_Hub :: struct {
    using base: Event_Broker,
}

central_message_hub_publish :: proc(topic: string, event: rawptr) {}
central_message_hub_subscribe :: proc(topic: string, handler: rawptr) {}

// ============================================================================
// 3. LIFECYCLE COMPONENT PATTERN
// ============================================================================
Lifecycle :: struct {
    start: proc(),
    stop: proc(),
}

Http_Server_Component :: struct {
    using base: Lifecycle,
    port: int,
}

http_server_start :: proc() {
    fmt.println("Starting HTTP Server")
}

http_server_stop :: proc() {
    fmt.println("Stopping HTTP Server")
}

// ============================================================================
// 4. ITERATOR PATTERN
// ============================================================================
Custom_Iterator :: struct {
    has_next: proc() -> bool,
    next: proc() -> rawptr,
}
