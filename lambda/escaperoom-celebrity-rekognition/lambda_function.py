 #*****************************************************
#                                                    *
# Copyright 2022 Amazon.com, Inc. or its affiliates. *
# All Rights Reserved.                               *
#                                                    *
#*****************************************************
""" Image Send Only """
import cv2
import base64
import boto3
import threading
 
class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(1)
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()
    # grab frames as soon as they are available
    def _reader(self):
        while True:
            ret = self.cap.grab()
            if not ret:
                break
    # retrieve latest frame
    def read(self):
        ret, frame = self.cap.retrieve()
        return frame
cap = VideoCapture(1)
def infinite_infer_run():
    """ Entry point of the lambda function"""
    try:
        while True:
            # Get a frame from the video stream
            frame = cap.read()
            if frame != "":
                retval, frame = cv2.imencode('.jpg', frame)
                base64_image = str(base64.b64encode(frame))
                base64_image = base64_image[:-1]
                base64_image = base64_image[2:]
                lambda_client = boto3.client('lambda')
                lambda_payload = '{ "base64_image": "'+base64_image+'"}'
                lambda_client.invoke(FunctionName='escaperoom-celebrity-rekognition-process',
                                    InvocationType='RequestResponse',
                                    Payload=lambda_payload)
                print("Image photo sent")
            else:
                print("Camera not ready")
    except Exception as ex:
        print(ex)

infinite_infer_run()