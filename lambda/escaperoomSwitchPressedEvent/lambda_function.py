import json
import boto3
 
def lambda_handler(event, context):
    mqttdata = boto3.client('iot-data')
    def activateRelay(gpio):
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )
    activateRelay(2)
    lambda_client = boto3.client('lambda')
    lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Passcode\\"}\"}'
    lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
    return { 'statusCode': 200, }