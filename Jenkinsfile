pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying ShopFlow...'

                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                kubectl rollout restart deployment/shopflow

                kubectl rollout status deployment/shopflow
                '''
            }
        }

        stage('Verification') {
            steps {
                sh '''
                kubectl get pods
                kubectl get svc
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline executed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
