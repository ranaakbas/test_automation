pipeline {
    agent any

    environment {
        BROWSERSTACK_USERNAME = credentials('browserstack-username')
        BROWSERSTACK_ACCESS_KEY = credentials('browserstack-access-key')
        USE_LOCAL = 'false'
        BS_APP_URL = credentials('bs-app-url')
    }
    
    stages {

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

    post {

        success {
            emailext(
                to: 'rana.akbas@mobiva.co',
                subject: "SUCCESS - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build sonucu: ${currentBuild.currentResult}\n${env.BUILD_URL}"
            )
        }

        failure {
            emailext(
                to: 'rana.akbas@mobiva.co',
                subject: "FAIL - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build sonucu: ${currentBuild.currentResult}\n${env.BUILD_URL}"
            )
        }

        always {
            echo "Pipeline finished with status: ${currentBuild.currentResult}"
        }
    }
}
