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
                sh './evalPolicyResult.py'
            }
        }
    }
}
