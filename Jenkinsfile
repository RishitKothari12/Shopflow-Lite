pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                echo "Using Jenkins SCM checkout"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shopflow:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                kubectl get pods
                kubectl get svc
                '''
            }
        }
    }
}
