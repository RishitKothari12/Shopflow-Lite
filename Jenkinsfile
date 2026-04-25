pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // This pulls your code from the current directory or GitHub
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker Image...'
                // Builds the image using your provided Dockerfile 
                sh 'docker build -t shopflow:latest .'
            }
        }

        stage('K8s Deployment') {
            steps {
                echo 'Deploying to Minikube...'
                // Applies your secret, deployment, and service files 
                sh 'kubectl apply -f k8s/secret.yaml'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                
                // Force a restart to pull the "latest" image
                sh 'kubectl rollout restart deployment/shopflow'
            }
        }
    }
}
