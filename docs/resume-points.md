# Supported Resume Points

- Implemented a declarative Jenkins CI/CD pipeline that tests, scans, publishes Git-SHA-tagged images to ECR, performs atomic Helm deployments, and validates Kubernetes rollout health.
- Built release-provenance endpoints exposing application version, commit SHA, and environment for evidence-based deployment verification.
- Added failure diagnostics, retained test reporting, concurrency controls, and rollback procedures for reliable delivery operations.
- Defined Terraform-managed immutable ECR storage and versioned S3 build artifacts with public-access blocking.
