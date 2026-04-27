pipeline {
    agent {
        // This tells Jenkins to spin up the temporary worker pod
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
                serviceAccountName: jenkins-deployer
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
        // Prevents the 10-minute timeout error you saw earlier
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Deep clone with extended timeout to bypass WSL network drops
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
                // We execute these commands INSIDE the temporary kubectl container
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
            cleanWs() // Cleans up the workspace to save memory
        }
        success {
            echo '✅ Pipeline Executed Successfully'
        }
        failure {
            echo '❌ Pipeline Failed'
        }
    }
}