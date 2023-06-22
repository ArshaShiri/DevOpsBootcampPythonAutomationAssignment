#!/usr/bin/env groovy

pipeline {
    agent any
    environment {
        // Used by get-images.py script
        ECR_REPO_NAME = 'java-maven-app'

        // Used by Boto3
        AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
        AWS_DEFAULT_REGION = 'eu-central-1'
    }

    stages {
        stage('select image version') {
            steps {
               script {
                  echo 'Fetching available image versions...'
                  def result = sh(script: 'python3 get-images.py', returnStdout: true).trim()
                  echo result
               }
            }
        }
    }
}
