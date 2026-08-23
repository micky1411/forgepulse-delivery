# Interview Guide

## Explain the pipeline

Jenkins checks out a commit, creates an isolated Python environment, lints and tests the code, builds an image tagged with the Git SHA, blocks high or critical vulnerabilities, publishes to ECR, and performs an atomic Helm upgrade. It then waits for Kubernetes rollout health and reports diagnostics if anything fails.

## How do you know the right release deployed?

The application exposes `/release`, which reports the image version, commit SHA, and environment. This allows a deployment check to compare runtime evidence with the pipeline's intended commit.

## How does rollback work?

Helm automatically rolls back a failed atomic upgrade. Operators can also select a known healthy revision using `helm history` and `helm rollback`, then validate Kubernetes readiness and the release endpoint.
