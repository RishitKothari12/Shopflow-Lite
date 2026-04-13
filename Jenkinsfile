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
                sh 'sudo docker build -t shopflow:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'sudo kubectl apply -f k8s/'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                sudo kubectl get pods
                sudo kubectl get svc
                '''
            }
        }
    }
}
