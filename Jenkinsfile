pipeline {
    agent {
        docker { image 'openpolicyagent/opa:0.12.0' }
    }
    stages {
        stage('Evaluate') {
            steps {
                sh 'eval --data /app --format=values data.contino.rules'
            }
        }
    }
}
