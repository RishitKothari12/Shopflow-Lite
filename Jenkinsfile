pipeline {
    agent any
    environment {
        KUBECONFIG = '/var/jenkins_home/.kube/config'
        K8S_SERVER = 'http://172.25.160.164:33037'
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
                sh "kubectl apply -f k8s/secret.yaml --server=${K8S_SERVER} --validate=false"
                sh "kubectl apply -f k8s/deployment.yaml --server=${K8S_SERVER} --validate=false"
                sh "kubectl apply -f k8s/service.yaml --server=${K8S_SERVER} --validate=false"
                sh "kubectl rollout restart deployment/shopflow --server=${K8S_SERVER}"
            }
        }
    }
}
