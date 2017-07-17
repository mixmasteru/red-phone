import boto3
import json

print('Loading function')

client = boto3.client('iot-data', region_name='eu-central-1')
red_topic = 'alert/redphone'


def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    message = json.loads(message)
    host = message['AlarmDescription']
    region = message['Region']

    iot_message = "Achtung! Der Server "+host+", in der Region "+region+ ", ist nicht erreichbar."

    # return message
    response = client.publish(
        topic=red_topic,
        qos=1,
        payload=json.dumps({"message": iot_message})
    )

    print(response)
    return True
