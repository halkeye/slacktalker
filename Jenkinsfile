pipeline {
  agent { docker { image 'python:3.7.3-stretch' } }
  environment {
    registry = "halkeye/slack-resurrect"
    registryCredential = 'dockerhub-halkeye'
    dockerImage = ''
    DATABASE_URL = 'sqlite://'
  }

  options {
    timeout(time: 10, unit: 'MINUTES')
    ansiColor('xterm')
  }

  stages {
    stage('Before Install') {
      steps {
        sh """
          pip install --upgrade pip
          pip install --upgrade setuptools
          pip install --upgrade pytest
          pip --version
          """
      }
    }

    stage('Install') {
      steps {
        sh "pip install -r dev_requirements.txt"
      }
    }

    stage('Lint') {
      steps {
        sh 'pylint --errors-only --rcfile=./pylintrc slack_resurrect | tee pylint.log'
      }
      post {
        always {
          recordIssues aggregatingResults: true, enabledForFailure: true, tools: [pyLint(pattern: 'pylint.log')]
        }
      }

    }

    stage('Test') {
      steps {
        sh 'py.test  --junitxml=pytest-report.xml --cov-report xml'
      }
      post {
        always {
          junit 'pytest-report.xml'
        }
      }
    }

    stage('Coverage') {
      steps {
        sh 'coverage xml -i'
      }
      post {
        always {
          cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '70, 0, 0', enableNewApi: true, failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
        }
      }
    }

    stage('Docker') {
      agent any
      stages {
        stage('Build') {
          steps {
            script {
              dockerImage = docker.build registry
            }
          }
        }

        stage('Deploy') {
          when { branch 'master' }
          steps {
            script {
              docker.withRegistry( '', registryCredential ) {
                dockerImage.push()
              }
            }
          }
        }
      }
    }
  }
  post {
    failure {
      emailext(
        attachLog: true,
        recipientProviders: [developers()],
        body: "Build failed (see ${env.BUILD_URL})",
        subject: "[JENKINS] ${env.JOB_NAME} failed",
      )
    }
  }
}
