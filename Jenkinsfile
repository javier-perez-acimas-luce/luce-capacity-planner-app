pipeline {

  agent {label 'python-slave' }

  stages {
      stage('Code pull') {
        steps {
          checkout scm
        }
      }

      stage('Build environment') {
        steps {
          echo 'Building virtualenv'
          sh ''' conda create --yes -n ${BUILD_TAG} python=3.6.5
                        source activate ${BUILD_TAG}
                        pip install -r requirements.txt
                    '''
        }
      }

      stage("Build") {
        steps {
          echo('Build project')
          sh ''' python setup.py bdist_egg '''
        }
      }

      stage('Test coverage') {
        steps{
          echo('Test coverage')
          sh '''source activate ${BUILD_TAG}
              pytest --junitxml=pytest-report.xml --cov=. --cov-report xml
           '''
        }
        post{
          always{
            step([$class: 'CoberturaPublisher',
                                autoUpdateHealth: false,
                                autoUpdateStability: false,
                                coberturaReportFile: 'coverage.xml',
                                failNoReports: false,
                                failUnhealthy: false,
                                failUnstable: false,
                                maxNumberOfBuilds: 10,
                                onlyStable: false,
                                sourceEncoding: 'ASCII',
                                zoomCoverageChart: false])
            }
        }
      }

      stage('Code Style') {
        steps{
          echo('Pylint analysis')
          sh ''' pylint src/* -r n --disable=bad-continuation,import-error,maybe-no-member \
           --msg-template=\"{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}\" | tee pylint-report.txt || true '''
          stash name: "first-stash"
        }
      }

      stage('Sonar') {
        agent any
        steps{
          unstash "first-stash"
          echo('SonarQube analysis')
          withSonarQubeEnv(credentialsId: 'sonar-token', installationName: 'sonar_sugus') {
              sh ''' /home/jenkins/.jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner_v4/bin/sonar-scanner -Dproject.settings=sonar-project.properties'''
          }
          echo('Waiting for sonar quality gate')
          timeout(time: 1, unit: 'HOURS') {
            waitForQualityGate abortPipeline: true
          }
        }
      }

      stage("Upload to nexus") {
        when {
          tag pattern: "v?[0-9]+\\.[0-9]+\\.[0-9]+", comparator: "REGEXP"
        }
        steps {
          sh '''
           twine upload -r nexus3 --repository-url https://nexus.luceit.es:2443/repository/pypi-snapshots/ dist/* \
           --username Servicio.nexus --password Passw0rd
          '''
        }
      }

  }
  environment {
    PATH = "/home/jenkins/miniconda3/condabin:/home/jenkins/miniconda3/bin:${env.PATH}"
  }
  options {
    // Keep the 10 most recent builds
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timestamps()
  }
  post {
    always {
      sh 'conda remove --yes -n ${BUILD_TAG} --all'
    }
  }
}