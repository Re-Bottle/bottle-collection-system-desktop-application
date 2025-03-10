from datetime import datetime
from awscrt import mqtt

from interface.aws import mqtt_connection_builder

# from aws import mqtt_connection_builder
import json

# from datetime import datetime
import os
import threading
import queue
import sys
import time

from typing import Any

INPUT_ENDPOINT = "akpp5wezqfiun-ats.iot.ap-south-1.amazonaws.com"
CA_FILE = "\\certificates\\root-CA.crt"
CERT = "\\certificates\\Raspberry_PI.cert.pem"
KEY = "\\certificates\\Raspberry_PI.private.key"
BASE_TOPIC = "bottle/"
PORT = 8883

received_count = 0
publish_count = 1
received_all_event = threading.Event()
instruction_queue: queue.Queue[str] = queue.Queue()
mqtt_connection: mqtt.Connection
current_directory = os.getcwd()


# Callback when connection is accidentally lost.
def on_connection_interrupted(
    connection: mqtt.Connection, error: Exception, **kwargs: Any
):
    """
    Callback triggered when the connection is interrupted.

    :param connection: The MQTT connection object.
    :param error: The error that caused the connection to be interrupted.
    :param kwargs: Additional arguments.
    """
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(
    connection: mqtt.Connection,
    return_code: mqtt.ConnectReturnCode,
    session_present: bool,
    **kwargs: Any,
) -> None:
    """
    Callback triggered when the connection is resumed.

    :param connection: The MQTT connection object.
    :param return_code: The connection return code.
    :param session_present: Whether the session was persisted.
    :param kwargs: Additional arguments.
    """
    print(
        f"Connection resumed. return_code: {return_code} session_present: {session_present}"
    )

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and session_present:
        print(
            f"Session persisted. Resubscribing to existing topics... {session_present}"
        )

        # Synchronously resubscribe to existing topics
        resubscribe_future, _ = connection.resubscribe_existing_topics()
        # resubscribe_results: Dict[str, Any] = resubscribe_future.result() or {}
        resubscribe_future.add_done_callback(on_resubscribe_complete)  # type: ignore
        # # Handle the result of the synchronous resubscription
        # print(f"Resubscribe results: {resubscribe_results}")
        # topics: List[Tuple[str, mqtt.QoS]] = resubscribe_results.get('topics', [])

        # for topic, qos in topics:
        #     if qos is None:
        #         sys.exit(f"Server rejected resubscribe to topic: {topic}")


def on_resubscribe_complete(resubscribe_future):  # type: ignore
    resubscribe_results = resubscribe_future.result()  # type: ignore
    print("Resubscribe results: {}".format(resubscribe_results))  # type: ignore

    for topic, qos in resubscribe_results["topics"]:  # type: ignore
        if qos is None:
            sys.exit("Server rejected resubscribe to topic: {}".format(topic))  # type: ignore


# Callback when the subscribed topic receives a message
def on_message_received(
    topic: str, payload: bytes, dup: bool, qos: int, retain: bool, **kwargs: Any
):
    print(
        f"DEBUG: Message received on {topic}, payload={payload.decode('utf-8')}, dup={dup}, qos={qos}, retain={retain}"
    )
    global received_count
    received_count += 1
    received_all_event.set()


# Callback when the connection successfully connects
def on_connection_success(
    connection: mqtt.Connection, callback_data: mqtt.OnConnectionSuccessData
):
    """
    Callback triggered when the connection is successfully established.

    :param connection: The MQTT connection object.
    :param callback_data: The callback
    """
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print(
        "Connection Successful with return code: {} session present: {}".format(
            callback_data.return_code, callback_data.session_present
        )
    )


# Callback when a connection attempt fails
def on_connection_failure(
    connection: mqtt.Connection, callback_data: mqtt.OnConnectionFailureData
):
    """
    Callback triggered when the connection attempt fails.

    :param connection: The MQTT connection object.
    :param callback_data: The callback data.
    """
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))


# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(
    connection: mqtt.Connection, callback_data: mqtt.OnConnectionClosedData
):
    print("Connection closed")


def connection(device_id: str = "Test"):
    """
    Connect to the MQTT server.

    :param device_id: The device ID.
    """
    global mqtt_connection
    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
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
    try:
        connect_future = mqtt_connection.connect()
        connect_future.result()

        print("Connected!")
        return mqtt_connection
    except Exception as e:
        print(f"Connection error: {e}")
        print(mqtt_connection.client_id)
        sys.exit(1)


def subscribe_topic(topic: str):
    """
    Subscribe to a topic.

    :param topic: The topic to subscribe to.
    """
    print("Subscribing to topic '{}'...".format(topic))
    try:
        subscribe_future, _ = mqtt_connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,  # type: ignore
            callback=on_message_received,
        )

        subscribe_result = subscribe_future.result(timeout=5)
        print(f"Subscription result: {subscribe_result}")
        if subscribe_result is not None:
            print("Subscribed with {}".format(str(subscribe_result.values())))
    except Exception as e:
        print(f"Error subscribing to topic: {e}")


def publish_message(topic: str, message: dict[str, str]):
    """
    Publish a message to a topic.

    :param topic: The topic to publish to.
    :param message: The message to publish
    """
    global mqtt_connection, publish_count
    message["count"] = str(publish_count)
    message_json = json.dumps(message)
    mqtt_connection.publish(
        topic=topic, payload=message_json, qos=mqtt.QoS.AT_LEAST_ONCE  # type: ignore
    )
    publish_count += 1


def publish_mqtt(device_id: str = "Test"):
    topic = f"{BASE_TOPIC}"
    # Connect to the MQTT server
    # connection(device_id)

    message = {
        "device_id": device_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
    }
    publish_message(topic, message)

    # print("Disconnecting...")
    # return mqtt_connection.disconnect().result()


def subscribe_mqtt(device_id: str = "Test"):
    topic = f"{BASE_TOPIC}"
    # Connect to the MQTT server
    connection(device_id)

    subscribe_topic(topic)

    # while True:
    #     result = ""
    #     try:
    #         result = instruction_queue.get(timeout=1)
    #     except queue.Empty:
    #         result = None

    #     if result == "exit":
    #         received_all_event.set()
    #         break

    #     received_all_event.wait(timeout=30)
    #     if not received_all_event.is_set():
    #         print("here")
    #         pass
    try:
        while True:
            time.sleep(1)
            received_all_event.wait(timeout=30)
            if not received_all_event.is_set():
                print("Connection lost. Attempting to reconnect...")
    except KeyboardInterrupt:
        print("Exiting...")

    print("Disconnecting...")
    return mqtt_connection.disconnect().result()


if __name__ == "__main__":
    subscribe_mqtt("5d2e2172-616a-44f2-98b9-f37301c685e9")
