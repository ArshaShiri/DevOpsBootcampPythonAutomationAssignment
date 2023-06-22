import boto3
import os

query_repository_name = os.environ['ECR_REPO_NAME']

ecr_client = boto3.client('ecr')
images = ecr_client.describe_images(
        repositoryName=query_repository_name
    )

image_tags = []
for image in images['imageDetails']:
    image_tags.append(image['imageTags'][0])

for image in image_tags:
    print(image)
