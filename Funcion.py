import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('EstadosTabla')
    
    response = table.scan()
    items = response['Items']
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # CORS
            'Content-Type': 'application/json'
        },
        'body': json.dumps(items)
    }