pipeline {
    agent any 

    environment {
        // This is the standard Docker gateway to the host machine
        MINIKUBE_SERVER = "https://172.17.0.1:32781"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls the latest code from your Shopflow-Lite GitHub repo
                checkout scm
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying Shopflow-Lite to Minikube at ${env.MINIKUBE_SERVER}..."
                sh '''
                    # 1. Download the kubectl binary locally for the agent to use
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    
                    # 2. Apply Kubernetes Manifests
                    # We use --insecure-skip-tls-verify because the Minikube cert is issued for 127.0.0.1
                    # We use --validate=false to prevent hangs during slow network lookups
                    ./kubectl apply -f k8s/deployment.yaml -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify \
                        --validate=false
                        
                    ./kubectl apply -f k8s/service.yaml -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify \
                        --validate=false
                    
                    # 3. Trigger a rolling restart to pull any new images
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
                    ./kubectl rollout status deployment/shopflow -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify
                        
                    ./kubectl get pods -n default \
                        --server=${MINIKUBE_SERVER} \
                        --insecure-skip-tls-verify
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline Executed Successfully. Shopflow-Lite is live!"
        }
        failure {
            echo "❌ Pipeline Failed. Check the console logs for connection or YAML errors."
        }
    }
}