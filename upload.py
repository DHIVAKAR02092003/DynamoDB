import json
import boto3

# Connect to DynamoDB in correct region
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Projects')  # Your table name

# Read and parse the JSON file
with open('project.txt', 'r') as file:
    data = json.load(file)  # This loads the whole array

# Loop through each project and upload
for project in data:
    try:
        table.put_item(Item=project)
        print(f"✅ Uploaded: {project['project_id']}")
    except Exception as e:
        print(f"❌ Failed to upload: {project.get('project_id', 'UNKNOWN')}")
        print(e)
