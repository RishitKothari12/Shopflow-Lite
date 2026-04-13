pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/RishitKothari12/Shopflow-Lite.git'
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
    }
}
