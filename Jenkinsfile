pipeline {
    agent any 

    environment {
        // Updated to your latest port: 32786
        // 172.17.0.1 is the bridge gateway from Docker to your WSL Host
        MINIKUBE_SERVER = "https://172.17.0.1:32786"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying Shopflow-Lite to Minikube at ${env.MINIKUBE_SERVER}..."
                sh '''
                    # 1. Get the kubectl binary
                    curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    
                    # 2. Apply Manifests
                    # --insecure-skip-tls-verify: Required because the certificate is issued for 127.0.0.1
                    # --server: Redirects the request from the container's localhost to the WSL Host
                    ./kubectl apply -f k8s/deployment.yaml -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify \
                        --validate=false
                        
                    ./kubectl apply -f k8s/service.yaml -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify \
                        --validate=false
                    
                    # 3. Force Restart Pods
                    ./kubectl rollout restart deployment/shopflow -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify
                '''
            }
        }

        stage('Verification') {
            steps {
                sh '''
                    ./kubectl get pods -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful!"
        }
        failure {
            echo "❌ Connection Refused. Check if Minikube is running with --apiserver-ips=172.17.0.1"
        }
    }
}