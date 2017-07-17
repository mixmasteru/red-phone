import os
import json
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from src.red_alert.config import iot_host
from src.red_alert.red_phone import RedPhone

realPath = os.path.realpath(__file__)
dirPath = os.path.dirname(realPath)+"/"
authPath = dirPath + "auth/"

topic = "alert/redphone"
rootCAPath = authPath + "root-CA.crt"
certificatePath = authPath + "redphone.cert.pem"
privateKeyPath = authPath + "redphone.private.key"

red_phone = RedPhone()


# Custom MQTT message callback
def custom_callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    msg = json.loads(message.payload)
    red_phone.alert(msg['message'])


myAWSIoTMQTTClient = AWSIoTMQTTClient("RedPhone")
myAWSIoTMQTTClient.configureEndpoint(iot_host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, custom_callback)
time.sleep(2)


try:
    while True:
        pass
except KeyboardInterrupt:
    print("Goodbye.")
