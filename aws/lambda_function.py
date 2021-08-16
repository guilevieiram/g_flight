import json
import requests

def lambda_handler(event, context):

    requests.get("https://g-flights-backend.herokuapp.com/send_flights")
    requests.get("https://g-flights-backend.herokuapp.com/update_flights")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
