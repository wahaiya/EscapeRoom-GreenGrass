import json
import boto3

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')
    lambda_payload = '{\"requestContext\" :{\"domainName\": \"z7kur16zgb.execute-api.eu-central-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Celebrity Not Recognized\\"}\"}'
    lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
    return { 'statusCode': 200, }