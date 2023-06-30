# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
# author: ocean wang
# 
# v 1.0.0 first version

import time
import traceback
import json
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest
)

import awsiot.greengrasscoreipc.model as model

import RPi.GPIO as GPIO

from time import sleep
import threading


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)







TIMEOUT = 10

ipc_client = awsiot.greengrasscoreipc.connect()

#ledpin = 40     # PWM pin connected to LED
#GPIO.setwarnings(False)                 #disable warnings
#GPIO.setmode(GPIO.BOARD)                #set pin numbering system
#GPIO.setup(ledpin,GPIO.OUT)

#pi_pwm = GPIO.PWM(ledpin,1000)          #create PWM instance with frequency
#pi_pwm.start(0)                         #start PWM of required Duty Cycle

# fanIDLE = 1


#Relay_GPIOs =[14,15,18,23,24,25,8,7,21]
Relay_GPIOs =[21,14,15,18,23,24,25,8,7,12,16,20,6,13]
def Relay_init():
    for gpio in Relay_GPIOs: #所有灯闪2次
        print(gpio)
        GPIO.setup(gpio, GPIO.OUT)
        GPIO.output(gpio, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(gpio, GPIO.LOW)
       
def writeRelay(relaynum, state):
    global Relay_GPIOs
    print("GPIO:",Relay_GPIOs[relaynum])
    print("State:",state)
    if state==1:  
        GPIO.output(Relay_GPIOs[relaynum], GPIO.HIGH)
    else:
        GPIO.output(Relay_GPIOs[relaynum], GPIO.LOW) 
        

def publishKeepAlive():
    PUBLISH_TOPIC  = "escaperoom_relay/pub"
    print("publishKeepAlive...")
    live_message =  {"KeepAlive": "ping"}
    op = ipc_client.new_publish_to_iot_core()
    op.activate(model.PublishToIoTCoreRequest(
            topic_name=PUBLISH_TOPIC,
	        qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(live_message).encode('utf8')))
    try:
           result = op.get_response().result(timeout=5.0)
           print("successfully published message:", result)
    except Exception as e:
           print("failed to publish message:", e)

class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()
  
    def on_stream_event(self, event: IoTCoreMessage) -> None:
        global fanIDLE
        try:
            message_received=str(event.message.payload, "utf-8")
            json_msg=json.loads(message_received)
            #topic_name = event.message.topic_name
            relay_num=int(json_msg['gpio'])
            state= int(json_msg['state']) 
            writeRelay(relay_num,state)          

            # Handle message
            #if fanIDLE == 1:
            #   fanIDLE = 0
            #   print("Starting new thread")
               # Create a thread from a function with arguments
            #   th = threading.Thread(target=spinFan, args=(1,))
               # Start the thread
            #   th.start()  


        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass


topic = "escaperoom_relay/sub"
qos = QOS.AT_MOST_ONCE

Relay_init() # 初始化继电器管脚状态 所有灯闪烁
#spin fan when component first starts
#spinFan(1)

request = SubscribeToIoTCoreRequest()
request.topic_name = topic
request.qos = qos
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_iot_core(handler)
operation.activate(request)
future_response = operation.get_response() 
future_response.result(TIMEOUT)

# Keep the main thread alive, or the process will exit.
while True:
    try:
        publishKeepAlive()
    except Exception as e:
           print("failed to call :publishKeepAlive", e)
           continue 
    time.sleep(5)                  
# To stop subscribing, close the operation stream.
operation.close()


