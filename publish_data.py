# Import the necessary modules and packages
import json
import requests
from datetime import datetime


# Defining the publish_data function containing the format in which data needs to be parsed
def publish_data():
    url = "http://127.0.0.1:5000/publish"  # Replace with your Flask app endpoint

    # Generate random data
    data = {
        "Header": {
            "TimeStamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
            "MsgId": 0,
            "MsgType": "",
            "ClientId": "",
            "MsgVer": "1.0.0",
        },
        "Data": {
            "EType": 0,
            "Id": 0,
            "Fb": 0,
            "P1": "1234",  # JobNumericId
            "P2": "786",  # caseId
            "P3": 0,  # TrayId
            "P4": 0,
            "P5": 0,
            "P6": 0,
            "P7": 0,
            "P8": 20,
            "P9": 0,  # DewaxTrayId
            "P10": 9,
            "P11": 0,
            "P12": 0,
            "P13": 0,
            "P14": 0,
            "P15": 0,
            "P16": 0,
            "P17": 0,
            "P18": 0,
            "P19": 0,
            "P20": 0,
        },
    }

    # Convert data to JSON string
    json_data = json.dumps(data)

    # Set headers for the request
    headers = {"Content-Type": "application/json"}

    # Send the POST request to your Flask app
    response = requests.post(url, data=json_data, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print("Data published successfully")
    else:
        print("Failed to publish data")


# Call the function for mock execution
publish_data()
