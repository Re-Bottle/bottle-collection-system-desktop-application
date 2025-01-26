from awscrt import mqtt
from aws import mqtt_connection_builder
import json
from datetime import datetime
import os
import threading
import sys
import queue

INPUT_ENDPOINT = "akpp5wezqfiun-ats.iot.ap-south-1.amazonaws.com"
CA_FILE = "\\certificates\\root-CA.crt"
CERT = "\\certificates\\Raspberry_PI.cert.pem"
KEY = "\\certificates\\Raspberry_PI.private.key"
BASE_TOPIC = "bottle"
PORT = 8883

received_count = 0
received_all_event = threading.Event()
instruction_queue: queue.Queue[str] = queue.Queue()
mqtt_connection: mqtt.Connection

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):  # type: ignore
    print("Connection interrupted. error: {}".format(error))  # type: ignore


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection:mqtt.Connection, return_code, session_present, **kwargs): # type: ignore
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present)) # type: ignore
    print(f"here: {session_present}")

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics() # type: ignore
        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete) # type: ignore


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs): # type: ignore
    print("Received message from topic '{}': {}".format(topic, payload)) # type: ignore
    global received_count
    received_count += 1
    
        
def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the connection successfully connects
def on_connection_success(connection:mqtt.Connection, callback_data):  # type: ignore
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print(
        "Connection Successful with return code: {} session present: {}".format(
            callback_data.return_code, callback_data.session_present
        )
    )


# Callback when a connection attempt fails
def on_connection_failure(connection:mqtt.Connection, callback_data): # type: ignore
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))


# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection:mqtt.Connection, callback_data): # type: ignore
    print("Connection closed")


def connection(device_id:str = "Test"):
    global mqtt_connection
    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(  # type: ignore
        endpoint=INPUT_ENDPOINT,
        port=PORT,
        cert_filepath=current_directory + CERT,
        pri_key_filepath=current_directory + KEY,
        ca_filepath=current_directory + CA_FILE,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=device_id,
        clean_session=False,
        keep_alive_secs=60,
        http_proxy_options=None,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed,
    )

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

def subscribe_topic(topic:str):
    print("Subscribing to topic '{}'...".format(topic))
    subscribe_future, _ = mqtt_connection.subscribe(
        topic=topic,
        qos=mqtt.QoS.AT_LEAST_ONCE, callback=on_message_received)# type: ignore 

    subscribe_result = subscribe_future.result()
    if subscribe_result is not None and subscribe_result['qos'] is not None:
        print("Subscribed with {}".format(str(subscribe_result.values())))

def publish_message(topic:str, message:dict[str, str]):
    global mqtt_connection
    message_json = json.dumps(message)
    mqtt_connection.publish(
        topic=topic, payload=message_json, qos=mqtt.QoS.AT_LEAST_ONCE  # type: ignore
    )

current_directory = os.getcwd()



def notify_bottle_detected(device_id:str = "Test"):
    topic = f"{BASE_TOPIC}/{device_id}"
    # Connect to the MQTT server
    connection(device_id)

    # Subscribe
    subscribe_topic(topic)


    # message = {
    #     "device_id": device_id,
    #     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    # }
    # publish_message(topic, {"device_id": device_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


    while True:
        result = ""
        try: 
            result = instruction_queue.get(timeout=1)
        except queue.Empty:
            result = None

        if result == "exit":
            received_all_event.set()
            break

        received_all_event.wait(timeout=30) 
        if not received_all_event.is_set():
            print("here")
            pass

        
    print("Disconnecting...")
    return mqtt_connection.disconnect().result()


if __name__ == "__main__":
    notify_bottle_detected("5d2e2172-616a-44f2-98b9-f37301c685e9")
    print("Disconnected!")
