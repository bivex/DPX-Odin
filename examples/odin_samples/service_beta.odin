package beta

import "alpha"

Beta_Service :: struct {
    alpha_client: ^alpha.Alpha_Service,
}

beta_service_run :: proc(self: ^Beta_Service) {}
