pipeline {
    agent any 

    environment {
        /* * FIXED PORT: 8443 
         * Ensure you started minikube with: 
         * minikube start --apiserver-port=8443 --apiserver-ips=172.17.0.1
         */
        MINIKUBE_SERVER = "https://172.17.0.1:8443"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls code from the GitHub repo defined in the Jenkins job
                checkout scm
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying Shopflow-Lite to Minikube at ${env.MINIKUBE_SERVER}..."
                sh '''
                    # 1. Download kubectl binary if not present
                    if [ ! -f ./kubectl ]; then
                        curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
                        chmod +x kubectl
                    fi
                    
                    # 2. Apply Kubernetes Manifests
                    # --insecure-skip-tls-verify is used because certificates are usually bound to 127.0.0.1
                    ./kubectl apply -f k8s/deployment.yaml -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify \
                        --validate=false
                        
                    ./kubectl apply -f k8s/service.yaml -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify \
                        --validate=false
                    
                    # 3. Force Restart to pull latest images/configs
                    ./kubectl rollout restart deployment/shopflow -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify
                '''
            }
        }

        stage('Verification') {
            steps {
                echo "Verifying deployment status..."
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
            echo "✅ Deployment Successful on port 8443!"
        }
        failure {
            echo "❌ Connection Refused."
            echo "👉 Fix: Ensure Minikube is running on the host with:"
            echo "   minikube start --apiserver-port=8443 --apiserver-ips=172.17.0.1"
        }
    }
}