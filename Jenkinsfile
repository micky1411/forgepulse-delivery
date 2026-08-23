pipeline {
  agent any
  options {
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 30, unit: 'MINUTES')
  }
  environment {
    AWS_REGION = 'us-east-1'
    ECR_REPOSITORY = 'forgepulse-dev'
    IMAGE_TAG = "${env.GIT_COMMIT ?: 'local'}"
    HELM_RELEASE = 'forgepulse'
    K8S_NAMESPACE = 'forgepulse-dev'
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Quality Gate') {
      steps {
        sh 'python3 -m venv .venv'
        sh '.venv/bin/pip install -e ".[dev]"'
        sh '.venv/bin/ruff check .'
        sh '.venv/bin/pytest -q --junitxml=test-results.xml'
      }
      post { always { junit allowEmptyResults: true, testResults: 'test-results.xml' } }
    }
    stage('Build') {
      steps { sh 'docker build --label org.opencontainers.image.revision=$GIT_COMMIT -t forgepulse:$IMAGE_TAG .' }
    }
    stage('Security Scan') {
      steps { sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL forgepulse:$IMAGE_TAG' }
    }
    stage('Publish ECR') {
      when { branch 'main' }
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-jenkins-oidc']]) {
          sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com'
          sh 'docker tag forgepulse:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG'
          sh 'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG'
        }
      }
    }
    stage('Deploy Dev') {
      when { branch 'main' }
      steps {
        sh 'helm upgrade --install $HELM_RELEASE helm/forgepulse --namespace $K8S_NAMESPACE --create-namespace --set image.repository=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY --set image.tag=$IMAGE_TAG --set release.gitSha=$GIT_COMMIT --atomic --timeout 5m'
      }
    }
    stage('Validate') {
      when { branch 'main' }
      steps {
        sh 'kubectl rollout status deployment/$HELM_RELEASE -n $K8S_NAMESPACE --timeout=180s'
        sh 'kubectl get pods -n $K8S_NAMESPACE'
      }
    }
  }
  post {
    failure {
      sh 'kubectl get events -n $K8S_NAMESPACE --sort-by=.lastTimestamp || true'
      sh 'kubectl logs -n $K8S_NAMESPACE -l app.kubernetes.io/name=forgepulse --tail=100 || true'
    }
    always { deleteDir() }
  }
}
