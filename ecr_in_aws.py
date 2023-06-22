import boto3
from operator import itemgetter

ecr_client = boto3.client('ecr')
repositories = ecr_client.describe_repositories()['repositories']

if len(repositories) == 0:
    print("Repository is empty!")

for repo in repositories:
    print(f"Repository name: {repo['repositoryName']}")

query_repository_name = "java-maven-app"

images = ecr_client.describe_images(
        repositoryName=query_repository_name
    )

image_tags = []

for image in images['imageDetails']:
    image_tags.append({
        'tag': image['imageTags'],
        'date': image['imagePushedAt']
    })

sorted_images_based_on_date = sorted(image_tags, key=itemgetter("date"), reverse=True)
for image in sorted_images_based_on_date:
    print(image)
