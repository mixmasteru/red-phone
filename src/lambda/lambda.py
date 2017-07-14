import boto3
import json

print('Loading function')

client = boto3.client('iot-data', region_name='eu-central-1')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    # return message
    response = client.publish(
        topic='alert/redphone',
        qos=1,
        payload=json.dumps({"message": message})
    )

    print(response)
    return True
