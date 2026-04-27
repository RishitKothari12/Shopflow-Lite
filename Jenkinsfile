pipeline {
    agent {
        kubernetes {
            websocket true
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
        success {
            echo '✅ Pipeline Executed Successfully'
        }
        failure {
            echo '❌ Pipeline Failed'
        }
    }
}