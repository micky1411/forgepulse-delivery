# Jenkins Setup

Use a dedicated Linux agent with Python 3.12, Docker, Trivy, AWS CLI, Helm, and kubectl. The controller should not execute builds.

Create credentials by identifier, never in the repository:

- `aws-jenkins-oidc`: an AWS credential integration backed by a least-privilege role.
- `AWS_ACCOUNT_ID`: a non-secret Jenkins environment value or managed configuration entry.
- A restricted kubeconfig or cloud-authenticated deployment identity for the development namespace.

Create a multibranch pipeline pointing at this repository and require pull requests for `main`. The Jenkinsfile publishes and deploys only from `main`. Production should use a separate protected stage and human approval.

The example AmazonWebServicesCredentialsBinding is broadly compatible but static key credentials are not recommended. In a real AWS-hosted agent, prefer an instance profile or workload identity and remove the binding.
