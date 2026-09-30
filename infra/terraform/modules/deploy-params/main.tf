# Deploy configuration in SSM Parameter Store, read by scripts/aws/_common.sh (load_env), so the
# scripts never need Terraform state.

resource "aws_ssm_parameter" "this" {
  for_each = var.parameters
  name     = "${var.path}/${each.key}"
  type     = "String"
  value    = each.value
}
