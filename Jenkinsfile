pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
                serviceAccountName: jenkins-deployer
            '''
        }
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [[
                        $class: 'CheckoutOption', 
                        timeout: 20
                    ], [
                        $class: 'CloneOption', 
                        timeout: 20,
                        noTags: true,
                        reference: '',
                        shallow: true,
                        depth: 1
                    ]], 
                    userRemoteConfigs: [[
                        url: 'https://github.com/RishitKothari12/Shopflow-Lite.git'
                    ]]
                ])
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying ShopFlow to Minikube...'
                sh '''
                curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
                chmod +x kubectl
                
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
                echo "Checking Pods..."
                ./kubectl get pods -n default
                echo "Checking Services..."
                ./kubectl get svc -n default
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline Executed Successfully'
        }
        failure {
            echo '❌ Pipeline Failed'
        }
    }
}