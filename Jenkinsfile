pipeline {
    agent any
    parameters {
        string(name: 'VAULT_ADDRESS', defaultValue: 'https://vault.nitin.guru:8200', description: 'The vault instance managing GCP accounts')
    }
    environment {
      TF_VAR_vault_address = "${params.VAULT_ADDRESS}"
      VAULT_TOKEN = credentials('VAULT_TOKEN')
      TF_CLI_CONFIG_FILE = "${env.WORKSPACE}/.terraformrc"
      GHE_ACCESS_TOKEN = credentials('ghe-anz-simon-personal-token')
      PULL_REQUEST_ID = "${env.ghprbPullId}"
    }
    stages {
        stage('Generate TF Plan') {
            environment {
                TFE_WORKSPACE_TOKEN = credentials('TFE_TEST_PROJECT_WORKSPACE_TOKEN')
            }
            steps {
                sh "./generateBackendConfig.sh ${env.TFE_WORKSPACE_TOKEN}"
                sh 'terraform init'
                sh "./genPlan.sh ${env.WORKSPACE}"
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
            junit '*-report.xml'
        }
        failure {
            script {
                sh 'pip3 install --user -r requirements.txt'
                sh "cat result.json | ./post_comment.py --access_token=${env.GHE_ACCESS_TOKEN} --hostname=ghe-poc.apac.squadzero.io --repo=contino-anz/test-project --pr=${env.PULL_REQUEST_ID}"
            }
        }
    }
}
