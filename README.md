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