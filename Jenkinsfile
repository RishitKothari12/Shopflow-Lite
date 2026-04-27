pipeline {
    // Spawns a temporary pod just for this build
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
                containers:
                - name: kubectl
                  image: bitnami/kubectl:latest
                  command:
                  - cat
                  tty: true
            '''
        }
    }

    options {
        // Fixes the timeout issue by giving Git more time and setting global timeouts
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Extended timeout and standard checkout instead of shallow
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
                        shallow: false
                    ]], 
                    userRemoteConfigs: [[
                        url: 'https://github.com/RishitKothari12/Shopflow-Lite.git'
                    ]]
                ])
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Run the commands inside the ephemeral 'kubectl' container
                container('kubectl') {
                    echo 'Deploying ShopFlow to Minikube...'
                    sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout restart deployment/shopflow
                    kubectl rollout status deployment/shopflow
                    '''
                }
            }
        }

        stage('Verification') {
            steps {
                container('kubectl') {
                    sh '''
                    echo "Checking Pods..."
                    kubectl get pods
                    echo "Checking Services..."
                    kubectl get svc
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Professional cleanup of the workspace after build
        }
        success {
            echo '✅ Pipeline Executed Successfully'
        }
        failure {
            echo '❌ Pipeline Failed'
        }
    }
}