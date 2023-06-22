#!/usr/bin/env groovy

pipeline {
    agent any
    environment {
        // Used by get-images.py and deploy.py script
        ECR_REPO_NAME = 'java-maven-app'

        ECR_REGISTRY = '849690659475.dkr.ecr.eu-central-1.amazonaws.com'

        // Used by deploy.py script
        EC2_SERVER = '3.121.196.12'
        EC2_USER = 'ec2-user'
        AWS_SSH_KEY = credentials('aws-ec2-ssh')
        DOCKER_USER = 'AWS'
        DOCKER_PWD = credentials('ecr-repo-pwd')
        CONTAINER_PORT = '8080'
        HOST_PORT = '8080'

        // Used by Boto3
        AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
        AWS_DEFAULT_REGION = 'eu-central-1'
    }

    stages {
        stage('Select image version') {
            steps {
               script {
                  echo 'Fetching available image versions...'
                  def result = sh(script: 'python3 get-images.py', returnStdout: true).trim()

                  // Split returns an Array, but choices expects either List or String, so we do "as List"
                  def tags = result.split('\n') as List
                  version_to_deploy = input message: 'Select version to deploy', ok: 'Deploy', parameters: [choice(name: 'Select version', choices: tags)]
                  echo "selected tag is: ${version_to_deploy}" 

                  // Construct full docker image name
                  env.DOCKER_IMAGE = "${ECR_REGISTRY}/${ECR_REPO_NAME}:${version_to_deploy}"
                  echo "Seclected image is: ${env.DOCKER_IMAGE}"
               }
            }
        }

        stage('Deploying image') {
            steps {
                script {
                   echo 'Deploying selected docker image to EC2...'
                   def result = sh(script: 'python3 deploy.py', returnStdout: true).trim()
                   echo result
                }
            }
        }
    }
}
