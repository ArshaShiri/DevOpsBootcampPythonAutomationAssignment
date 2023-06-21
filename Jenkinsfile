#!/usr/bin/env groovy

pipeline {
    agent any
    stages {
        stage('select image version') {
            steps {
               script {
                  echo 'fetching available image versions'
                  def result = sh(script: 'python3 get-images.py', returnStdout: true).trim()
               }
            }
        }
    }
}
