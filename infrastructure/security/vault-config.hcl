# infrastructure/security/vault-config.hcl
path "secret/data/nexusguard/*" {
  capabilities = ["read", "list"]
}
