pipeline {
    agent { label 'windows' }
    options { timestamps(); timeout(time: 40, unit: 'MINUTES') }
    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser')
    }
    environment {
        RF_TEST_EMAIL = credentials('automationexercise-test-email')
        RF_TEST_PASSWORD = credentials('automationexercise-test-password')
        RF_TEST_NAME = 'Sayantana Halder'
    }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Install') {
            steps { bat '''py -m venv .venv
call .venv\\Scripts\\activate.bat
python -m pip install -r requirements.txt''' }
        }
        stage('Run Robot') {
            steps {
                bat '''call .venv\\Scripts\\activate.bat
robot --variable BROWSER:%BROWSER% --outputdir Results TestSuites/02_login_tests.robot TestSuites/03_ecommerce_business_flow.robot'''
            }
        }
    }
    post {
        always {
            step([$class: 'RobotPublisher', outputPath: 'Results', outputFileName: 'output.xml',
                  reportFileName: 'report.html', logFileName: 'log.html',
                  disableArchiveOutput: false, passThreshold: 100, unstableThreshold: 90])
            archiveArtifacts artifacts: 'Results/**', allowEmptyArchive: true
        }
    }
}
