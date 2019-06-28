pipeline {
  agent { docker { image 'python:3.7.3-stretch' } }

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
        sh 'pylint --rcfile=./pylintrc CODE > pylint.log'
				recordIssues aggregatingResults: true, enabledForFailure: true, tools: [pyLint(pattern: 'pylint.log')]
      }
    }

    stage('Test') {
      steps {
        sh 'py.test  --junitxml=pytest-report.xml'
        sh 'coverage xml -i'
      }
    }

    stage('Docker') {
      agent any
      stages {
        stage('Build') {
          steps {
            sh 'docker build -t halkeye/slack-foodee .'
          }
        }

        stage('Deploy') {
          when { branch 'master' }
          environment { DOCKER = credentials('dockerhub-halkeye') }
          steps {
            sh 'docker login --username $DOCKER_USR --password=$DOCKER_PSW'
            sh 'docker push halkeye/slack-foodee'
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
