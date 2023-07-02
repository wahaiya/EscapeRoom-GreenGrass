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
    
    def led_flash(gpio):
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )

    def red_flash(gpio): # 红灯闪烁3次 
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "1"}) )
      time.sleep(1)
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
    def led_off(gpio):
      response = mqttdata.publish( topic='escaperoom_relay/sub', qos=1, payload=json.dumps({"gpio": ""+str(gpio)+"","state": "0"}) )
    def led_on(gpio):
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
        activateRelay(2) # 第二关 输入正确密码 灯箱2号亮
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Celebrity\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('Password OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "reset":
        #activateRelay(6)
        #重新设置密码 
        led_off(0)
        led_off(1)
        led_off(2)
        led_off(3)
        led_off(4)
        led_off(5)
        led_off(6)
        led_off(7)
        led_off(8)
        led_off(9)
        led_off(10)
        led_off(11)

        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Reset\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        lambda_client.invoke(FunctionName='shuffleQuestions', InvocationType='Event')
      
      elif password == "passcode":
        # Switch 按键被按下 
        # activateRelay(1) 第一关 按下switch 键  1号灯箱亮 
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Passcode\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
      elif password == "celebrity":
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Celebrity\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        # 进入第三关 ， 灯箱3 闪烁一下  
        # led_flash(3) 
      elif password == "questionRight":
        
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"questionRight\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        # 灯箱4号绿灯闪烁
        led_flash(4)
        return {
          'statusCode': 200,
          'body': json.dumps('questionRight OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "questionWrong":
        # 红灯量闪烁（11）
        red_flash(11)
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
        
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"challengeCompleted\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        lambda_client.invoke(FunctionName='shuffleQuestions', InvocationType='Event')
    
        # 从1到8的灯闪烁 1 次 
        led_flash(1)
        led_flash(2)
        led_flash(3)
        led_flash(4)
        led_flash(5)
        led_flash(6)
        led_flash(7)
        led_flash(8)
        
        led_off(9)
        led_off(10)
        led_off(11)
        led_on(1)
        led_on(2)
        led_on(3)
        led_on(4)
        led_on(5)
        led_on(6)
        led_on(7)
        led_on(8)
        
        
        return {
          'statusCode': 200,
          'body': json.dumps('challengeCompleted OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "celebrityDetected":
        # 检测通过
      
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"OK - Authorized Personnel Detected\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        activateRelay(3) 
        return {
          'statusCode': 200,
          'body': json.dumps('celebrityDetected OK'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }
      elif password == "timeUp":
        #activateRelay(6)
        # 显示红色 （9-11） 
        activateRelay(9)
        activateRelay(10)
        activateRelay(11)
        led_off(1)
        led_off(2)
        led_off(3)
        led_off(4)
        led_off(5)
        led_off(6)
        led_off(7)
        led_off(8)
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
        activateRelay(0)
        led_off(1)
        led_off(2)
        led_off(3)
        led_off(4)
        led_off(5)
        led_off(6)
        led_off(7)
        led_off(8)
        led_off(9)
        led_off(10)
        led_off(11)
        
        
        # 触摸屏边上的灯柱启动闪烁
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
        # 密码错误 
        # 2号灯箱 红色闪烁 3次 
        red_flash(10)  
        lambda_payload = '{\"requestContext\" :{\"domainName\": \"6n5wzcue6h.execute-api.ap-northeast-1.amazonaws.com\",\"stage\" : \"production\"}, \"body\": \"{\\"message\\":\\"Password ERROR\\"}\"}'
        lambda_client.invoke(FunctionName='escaperoom-SendMessageHandlerDFBBCD6B-YQfevSlei6XW', InvocationType='RequestResponse', Payload=lambda_payload)
        return {
          'statusCode': 200,
          'body': json.dumps('Password ERROR'),
          'headers': { 'Access-Control-Allow-Origin': '*'}
          }

    
