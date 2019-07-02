pipeline {
    agent any
    environment {
      TF_VAR_vault_address = "${VAULT_ADDRESS}"
      VAULT_TOKEN = credentials('VAULT_TOKEN')
      TF_CLI_CONFIG_FILE = "${env.WORKSPACE}/.terraformrc"
    }
    stages {
        stage('Generate TF Plan') {
            steps {
                sh './generateBackendConfig.sh credentials('TFE_TEST_PROJECT_WORKSPACE_TOKEN')
                sh 'terraform init'
                sh './genPlan.sh'
            }
        }
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
