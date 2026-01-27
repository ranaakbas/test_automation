pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Repo başarıyla çekildi'
            }
        }

        stage('Environment Check') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version
                '''
            }
        }
    }
}
