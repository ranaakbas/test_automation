pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📦 Repo çekildi'
            }
        }

        stage('Setup Python Env') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest
                '''
            }
        }
    }
}
