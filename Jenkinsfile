pipeline {
    agent any
    stages {
        stage('Evaluate') {
            steps {
                sh './evalOpaPolicies.sh > result.json'
            }
        }
        stage('Interpret') {
            steps {
                sh 'pip3 install --user -r requirements.txt'
                sh './evalPolicyResult.py'
            }
        }
    }
    post {
        always {
            junit 'test-policy-result-report.xml'
        }
    }
}
