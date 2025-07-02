import boto3
import json
import configparser
import os

def extract():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.ini')
    config.read(config_path)

    region = config['aws']['region']
    table_name = config['aws']['table_name']

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response.get('Items', [])

    with open('raw_data.json', 'w') as f:
        json.dump(items, f, indent=2)    #into Json format

    print(f"Extracted {len(items)} items from DynamoDB")
