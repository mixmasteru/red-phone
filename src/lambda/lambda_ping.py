import os

hostname = ".eu-central-1.compute.internal"


def lambda_handler(event, context):

    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        print(hostname+' is up!')
        return True
    else:
        raise ConnectionError(hostname+' is down!')
