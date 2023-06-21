# DevOps Bootcamp Python Automation Assignment

## EXERCISE 1: Working with Subnets in AWS
* Get all the subnets in your default region
* Print the subnet Ids

**Solution:**

`subnets_in_aws.py`

## EXERCISE 2: Working with IAM in AWS
* Get all the IAM users in your AWS account
* For each user, print out the name of the user and when they were last active (hint: Password Last Used attribute)
* Print out the user ID and name of the user who was active the most recently

**Solution:**

`iam_in_aws.py`

## EXERCISE 3: Automate Running and Monitoring Application on EC2 instance
Write Python program which automatically creates EC2 instance, install Docker inside and starts Nginx application as Docker container and starts monitoring the application as a scheduled task. Write the program with the following steps:

* Start EC2 instance in default VPC
* Wait until the EC2 server is fully initialized
* Install Docker on the EC2 server
* Start nginx container
* Open port for nginx to be accessible from browser
* Create a scheduled function that sends request to the nginx application and checks the status is OK
* If status is not OK 5 times in a row, it restarts the nginx application

**Solution:**

* Make sure port 22(ssh) is open in the default security group in the default VPC
* Make sure a key-pair is available for the ec2 instance. The private key is then used to connect to the server

`running_and_monitoring_app_on_ec2.py`

## EXERCISE 4: Working with ECR in AWS

* Get all the repositories in ECR
* Print the name of each repository
* Choose one specific repository and for that repository, list all the image tags inside, sorted by date. Where the most recent image tag is on top

**Solution:**

`ecr_in_aws.py`

## EXERCISE 5: Python in Jenkins Pipeline

Create a Jenkins job that fetches all the available images from your application's ECR repository using Python. It allows the user to select the image from the list through user input and deploys the selected image to the EC2 server using Python.

**Instructions**

Do the following preparation manually:

* Start EC2 instance and install Docker on it
* Install Python, Pip and all needed Python dependencies in Jenkins
* Create 3 Docker images with tags 1.0, 2.0, 3.0 from one of the previous projects


Once all the above is configured, create a Jenkins Pipeline with the following steps:

1. Fetch all 3 images from the ECR repository (using Python)
2. Let the user select the image from the list (hint: https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/)
3. SSH into the EC2 server (using Python)
4. Run docker login to authenticate with ECR repository (using Python)
5. Start the container from the selected image from step 2 on EC2 instance (using Python)
6. Validate that the application was successfully started and is accessible by sending a request to the application (using Python)

**Solution:**

## ECR Creation

![image](https://github.com/ArshaShiri/DevOpsBootcampPythonAutomationAssignment/assets/18715119/81f02b9b-7233-4af7-b160-006d0838623a)

## Adding Docker Images to ECR

We use the java maven application for this section.

