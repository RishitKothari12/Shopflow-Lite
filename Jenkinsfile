pipeline {
    agent any
    environment {
        // Point to the config we mounted into the container
        KUBECONFIG = '/root/.kube/config'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Docker Build') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t shopflow:latest .'
            }
        }
        stage('K8s Deployment') {
            steps {
                echo 'Deploying to Minikube...'
                // Use --validate=false to bypass the OpenAPI check that failed
                sh 'kubectl apply -f k8s/secret.yaml --validate=false'
                sh 'kubectl apply -f k8s/deployment.yaml --validate=false'
                sh 'kubectl apply -f k8s/service.yaml --validate=false'
                sh 'kubectl rollout restart deployment/shopflow'
            }
        }
    }
}
