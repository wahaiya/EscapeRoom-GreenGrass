# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
# author: ocean


import time
import json
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client

from awsiot.greengrasscoreipc.model import (
    SubscribeToTopicRequest,
    SubscriptionResponseMessage
)

import awsiot.greengrasscoreipc.model as model
import os


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
swi = 37
TIMEOUT = 10
GPIO.setup(swi, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ipc_client = awsiot.greengrasscoreipc.connect()

def switch(channel):  
    if GPIO.input(channel):    # 高电平的开关松开
        print("release")
    else:                      # 低电平为开关按下
        publishMessage()
        print("pressed")

publish_topic="escaperoom_switch/pub"
subscribe_topic="escaperoom_switch/sub"

def publishMessage():
    press_message =  {"pressed": "yes"}
    op = ipc_client.new_publish_to_iot_core()
    op.activate(model.PublishToIoTCoreRequest(
            topic_name=publish_topic,
	        qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(press_message).encode('utf8')))
    try:
           result = op.get_response().result(timeout=5.0)
           print("successfully published message:", result)
           print(publish_topic)
           print(press_message)
    except Exception as e:
           print("failed to publish message:", e)

def publishKeepAlive():
    print("publishKeepAlive...")
    live_message =  {"KeepAlive": "ping"}
    op = ipc_client.new_publish_to_iot_core()
    op.activate(model.PublishToIoTCoreRequest(
            topic_name=publish_topic,
	        qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(live_message).encode('utf8')))
    try:
           result = op.get_response().result(timeout=5.0)
           print("successfully published message:", result)
    except Exception as e:
           print("failed to publish message:", e)


GPIO.add_event_detect(swi, GPIO.BOTH, callback=switch, bouncetime=200)

while True:
    time.sleep(1)
    publishKeepAlive()


