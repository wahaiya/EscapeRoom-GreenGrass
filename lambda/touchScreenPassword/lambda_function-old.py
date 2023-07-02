import json
import boto3
import time

def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')
    dynamodb = boto3.client('dynamodb')
    mqttdata = boto3.client('iot-data')
    def activateRelay(gpio):
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
      time.sleep(2)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )
      
    
    
    if 'queryStringParameters' in event and 'completedTime' in event['queryStringParameters']:
      completedTime =  event["queryStringParameters"]['completedTime']
      lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Completed time: '+ completedTime +'\\"}\"}'
      lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
      lambda_client.invoke(FunctionName='shuffleQuestions', InvocationType='Event')
      gameId = int(time.time()) 
      gameId = str(gameId)
      dynamodb.put_item(TableName='escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9', Item={'gameId':{'N':gameId},'completedTime':{'N':completedTime}})
      return {
        'statusCode': 200,
        'body': json.dumps('completedTime OK'),
        'headers': { 'Access-Control-Allow-Origin': '*'}
        }

    if 'queryStringParameters' in event and 'password' in event['queryStringParameters']:
      password =  event["queryStringParameters"]['password']
      if password == "297286":
        activateRelay(3)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Celebrity\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('Password OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "reset":
        activateRelay(7)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Reset\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        lambda_client.invoke(FunctionName='shuffleQuestions', InvocationType='Event')
      elif password == "passcode":
        activateRelay(2)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Passcode\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
      elif password == "celebrity":
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Celebrity\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
      elif password == "questionRight":
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"questionRight\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('questionRight OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "questionWrong":
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"questionWrong\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('questionWrong OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "nextQuestion":
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"nextQuestion\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('nextQuestion OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "challengeCompleted":
        activateRelay(5)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"challengeCompleted\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        lambda_client.invoke(FunctionName='shuffleQuestions', InvocationType='Event')
        return {
          'statusCode': 200,
          'body': json.dumps('challengeCompleted OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "celebrityDetected":
        activateRelay(4)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"OK - Authorized Personnel Detected\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('celebrityDetected OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "timeUp":
        activateRelay(6)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"timeUp\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        lambda_client.invoke(FunctionName='shuffleQuestions', InvocationType='Event')
        gameId = int(time.time()) 
        gameId = str(gameId)
        dynamodb.put_item(TableName='escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9', Item={'gameId':{'N':gameId},'completedTime':{'N':'99999'}})
        return {
          'statusCode': 200,
          'body': json.dumps('timeUp OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "switchCode":
        activateRelay(1)
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"switchCode\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        gameId = int(time.time()) 
        gameId = str(gameId)
        dynamodb.put_item(TableName='escaperoom-GamesTable8000B8A1-6LFZ1GJM4KI9', Item={'gameId':{'N':gameId},'completedTime':{'N':'99999'}})
        return {
          'statusCode': 200,
          'body': json.dumps('timeUp OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }

      else:
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Password ERROR\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('Password ERROR'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }

    
