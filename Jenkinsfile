pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/RishitKothari12/Shopflow-Lite.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shopflow .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
