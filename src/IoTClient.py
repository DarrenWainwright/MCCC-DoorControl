# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import time
import threading
import os
import json
from dotenv import load_dotenv
from SimpleDoor import SimpleDoor

# Load env vars
load_dotenv()

CONNECTION_STRING = os.getenv("IOT_HUB_CONNECTION")
MOTOR_MAX_RUNTIME = float(os.getenv("MOTOR_MAX_RUNTIME"))
Door = SimpleDoor()

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def device_method_listener(device_client):

    while True:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )  
        if method_request.name == "DoorAction":
            try:
                action = method_request.payload["action"]
                if action == "open":
                    Door.open(MOTOR_MAX_RUNTIME)
                elif action == "close":
                    Door.close(MOTOR_MAX_RUNTIME)
                else:
                    print("Unknown action " + action)

                response_payload = {"Response": "Executed Direct method {}".format(method_request.name)}
                response_status = 200
            except Exception as e:
                print('uh oh... went wrong..')
                print(e)

            response_payload = {"Response": "Executed Direct method {}".format(method_request.name)}
            response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)

        # if method_request.name == "SetTelemetryInterval":
        #     try:
        #         INTERVAL = int(method_request.payload)
        #     except ValueError:
        #         response_payload = {"Response": "Invalid parameter"}
        #         response_status = 400
        #     else:
        #         response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
        #         response_status = 200
        # else:
        #     response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
        #     response_status = 404

        # method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        # device_client.send_method_response(method_response)



def iothub_client_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Start a thread to listen 
        device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
        device_method_thread.daemon = True
        device_method_thread.start()

        while True:
            time.sleep(1)
        # while True:
        #     # Build the message with simulated telemetry values.
        #     temperature = TEMPERATURE + (random.random() * 15)
        #     humidity = HUMIDITY + (random.random() * 20)
        #     msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
        #     message = Message(msg_txt_formatted)

        #     # Add a custom application property to the message.
        #     # An IoT hub can filter on these properties without access to the message body.
        #     if temperature > 30:
        #       message.custom_properties["temperatureAlert"] = "true"
        #     else:
        #       message.custom_properties["temperatureAlert"] = "false"

        #     # Send the message.
        #     print( "Sending message: {}".format(message) )
        #     client.send_message(message)
        #     print( "Message sent" )
        #     time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Client for MCCC Door Control Starting.." )
    print ( "Press Ctrl-C to exit" )
    iothub_client_run()