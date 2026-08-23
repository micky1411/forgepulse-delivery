module "delivery_foundation" {
  source      = "../../modules/delivery-foundation"
  name        = "forgepulse-${var.environment}"
  environment = var.environment
}
