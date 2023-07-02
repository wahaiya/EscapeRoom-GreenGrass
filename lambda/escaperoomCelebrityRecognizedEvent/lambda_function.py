import json
import boto3
import time 
mqttdata = boto3.client('iot-data')
def activateRelay(gpio):
  response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
  time.sleep(2)
  response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')
    activateRelay(4)
    time.sleep(5)
    lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"OK - Authorized Personnel Detected\\"}\"}'
    lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
    return { 'statusCode': 200, }