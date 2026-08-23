# Delivery Security

- Jenkins receives credentials from its credential store, never source control.
- ECR tags are immutable and images must pass a high/critical Trivy gate.
- Containers and pods run as non-root with no added Linux capabilities.
- Helm `--atomic` prevents a failed release from remaining active.
- Terraform state and variable files are ignored because they may contain sensitive metadata.

Production hardening should add ephemeral Jenkins agents, signed images and admission verification, OIDC federation, namespace-scoped deploy permissions, audit log retention, and separated production approval.
