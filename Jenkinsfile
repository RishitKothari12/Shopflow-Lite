pipeline {
    agent any 
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying Shopflow-Lite to Minikube...'
                sh '''
                    # Download kubectl directly into the Jenkins workspace
                    curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl
                    chmod +x kubectl
                    
                    # Deploy to Minikube using the mounted credentials
                    ./kubectl apply -f k8s/deployment.yaml -n default
                    ./kubectl apply -f k8s/service.yaml -n default
                    ./kubectl rollout restart deployment/shopflow -n default
                    ./kubectl rollout status deployment/shopflow -n default
                '''
            }
        }
        stage('Verification') {
            steps {
                sh '''
                    ./kubectl get pods -n default
                    ./kubectl get svc -n default
                '''
            }
        }
    }
}