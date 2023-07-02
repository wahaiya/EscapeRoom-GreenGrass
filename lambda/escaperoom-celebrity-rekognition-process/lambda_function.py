import json
import boto3
import base64
import io
import cv2
import numpy as np
from PIL import Image

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition', region_name='ap-northeast-1')
    mqttmessage = boto3.client('iot-data', region_name='ap-northeast-1')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('escaperoom-ImageTable8000B8A1-6LFZ1GJM4KI9')
    data = event['base64_image']   
    base64_decoded = base64.b64decode(data)
    image = Image.open(io.BytesIO(base64_decoded))
    opencv_img= cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

    text_image = Image.fromarray(opencv_img)
    text_bytes_arr = io.BytesIO()
    text_image.save(text_bytes_arr, format='JPEG')
    text_bytes = text_bytes_arr.getvalue()
    response = rekognition.recognize_celebrities(
    Image={'Bytes':text_bytes})
    print('procesing image ....')
    if response['CelebrityFaces']:
        if response['CelebrityFaces'][0]['Name'] == "Werner Vogels":
            status = "OK - Authorized Personnel Detected"
            responsemqtt = mqttmessage.publish( topic='$aws/things/escaperoom/celebrityrekognition/status', qos=1, payload=json.dumps({"status":status}) )
            cv2.putText(opencv_img, status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,  0.8, (0, 255, 0), 3)
            retval, buffer = cv2.imencode('.jpg', cv2.resize(opencv_img, (1280, 736)))
            base64_image = str(base64.b64encode(buffer))
            base64_image = base64_image[:-1]
            base64_image = base64_image[2:]
            table.update_item(Key={"key": "cameraImage",},UpdateExpression="set image = :g",ExpressionAttributeValues={':g': json.dumps(base64_image)},ReturnValues="UPDATED_NEW")  
            return status
    else:
        status = "ERROR - No Authorized Personnel Detected"
        responsemqtt = mqttmessage.publish( topic='$aws/things/escaperoom/celebrityrekognition/status', qos=1, payload=json.dumps({"status":status}) )
        cv2.putText(opencv_img, status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,  0.8, (0, 0, 255), 3)
        retval, buffer = cv2.imencode('.jpg', cv2.resize(opencv_img, (1280, 736)))
        base64_image = str(base64.b64encode(buffer))
        base64_image = base64_image[:-1]
        base64_image = base64_image[2:]
        table.update_item(Key={"key": "cameraImage",},UpdateExpression="set image = :g",ExpressionAttributeValues={':g': json.dumps(base64_image)},ReturnValues="UPDATED_NEW")
        print('NO Authorized person update new environment ')
        return status
    
    

    

