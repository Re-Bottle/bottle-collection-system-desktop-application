from awscrt import mqtt
from interface.aws import mqtt_connection_builder
import json
from datetime import datetime
import os


# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):  # type: ignore
    print("Connection interrupted. error: {}".format(error))  # type: ignore


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):  # type: ignore
    print(
        "Connection resumed. return_code: {} session_present: {}".format(
            return_code, session_present  # type: ignore
        )
    )


# Callback when the connection successfully connects
def on_connection_success(connection, callback_data):  # type: ignore
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print(
        "Connection Successful with return code: {} session present: {}".format(
            callback_data.return_code, callback_data.session_present
        )
    )


# Callback when a connection attempt fails
def on_connection_failure(connection, callback_data):  # type: ignore
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))


# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection, callback_data):  # type: ignore
    print("Connection closed")


INPUT_ENDPOINT = "akpp5wezqfiun-ats.iot.ap-south-1.amazonaws.com"
CA_FILE = "\\certificates\\root-CA.crt"
CERT = "\\certificates\\Raspberry_PI.cert.pem"
KEY = "\\certificates\\Raspberry_PI.private.key"
TOPIC = "bottle"
PORT = 8883

current_directory = os.getcwd()


def notify_bottle_detected(device_id="Pearl"):  # type: ignore
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
        keep_alive_secs=30,
        http_proxy_options=None,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed,
    )

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    message = {
        "device_id": device_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    message_json = json.dumps(message)
    mqtt_connection.publish(
        topic=TOPIC, payload=message_json, qos=mqtt.QoS.AT_LEAST_ONCE  # type: ignore
    )

    return mqtt_connection.disconnect().result()


if __name__ == "__main__":
    notify_bottle_detected()
