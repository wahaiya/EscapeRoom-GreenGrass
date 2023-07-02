import json
import boto3

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')
    lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"EscapeRoomRelay\\"}\"}'
    lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
    return { 'statusCode': 200, }