package alpha

import "beta"

Alpha_Service :: struct {
    beta_client: ^beta.Beta_Service,
}

alpha_service_run :: proc(self: ^Alpha_Service) {}
