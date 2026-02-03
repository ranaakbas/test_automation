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

         stage('Run Android Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/android \
                        --junitxml=reports/junit.xml \
                        -v -ra
                '''
            }
        }
    }

    post {
    always {
        junit 'reports/junit.xml'
    }

    success {
        emailext(
            to: 'rana.akbas@mobiva.co',
            subject: "✅ Android Automation PASSED - Build #${BUILD_NUMBER}",
            body: """
📊 Android Automation Test Report

Job: ${JOB_NAME}
Build: #${BUILD_NUMBER}

-------------------------
Test Summary
-------------------------
Total Tests: ${TEST_COUNTS.total}
Passed: ${TEST_COUNTS.pass}
Failed: ${TEST_COUNTS.fail}
Skipped: ${TEST_COUNTS.skip}

Build URL:
${BUILD_URL}
"""
        )
    }

    failure {
        emailext(
            to: 'rana.akbas@mobiva.co',
            subject: "❌ Android Automation FAILED - Build #${BUILD_NUMBER}",
            body: """
📊 Android Automation Test Report

Job: ${JOB_NAME}
Build: #${BUILD_NUMBER}

-------------------------
Test Summary
-------------------------
Total Tests: ${TEST_COUNTS.total}
Passed: ${TEST_COUNTS.pass}
Failed: ${TEST_COUNTS.fail}
Skipped: ${TEST_COUNTS.skip}

-------------------------
❌ Failed Tests
-------------------------
${FAILED_TESTS}

Build URL:
${BUILD_URL}
"""
        )
    }
}
}