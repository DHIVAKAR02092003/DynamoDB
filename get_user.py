import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('User-data')

response = table.get_item(
    Key={
        'Name': 'User-1',
        'Age': 24
    }
)

item = response.get('Item')
if item:
    print("✅ Item found:")
    print(item)
else:
    print("❌ Item not found.")
