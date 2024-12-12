import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Configuration
THING_NAME = "my-device-thing"  # Replace with your Thing name
ENDPOINT = "akpp5wezqfiun-ats.iot.ap-south-1.amazonaws.com"  # AWS IoT Core endpoint
ROOT_CA = "./AmazonRootCA1.pem"  # Path to the Amazon Root CA
CERT_FILE = "./shared-claim-certificate.pem.crt"  # Path to the claim certificate
PRIVATE_KEY = (
    "claim-certificate-private.pem.key"  # Path to the claim certificate private key
)
TEMPLATE_NAME = "Raspberry_pi_Provisioning_Template"  # Replace with your Fleet Provisioning template name

# MQTT Topics
PROVISIONING_TOPIC = f"$aws/provisioning-templates/{TEMPLATE_NAME}/provision"
RESPONSE_TOPIC = f"$aws/provisioning-templates/{TEMPLATE_NAME}/provision/+"

# Initialize MQTT Client
mqtt_client = AWSIoTMQTTClient("ProvisioningClient")
mqtt_client.configureEndpoint(ENDPOINT, 8883)
mqtt_client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite queue
mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec


# Provisioning Response Callback
def on_provisioning_response(client, userdata, message):
    print("Received provisioning response")
    response = json.loads(message.payload)
    print(json.dumps(response, indent=4))

    if "certificatePem" in response:
        print("Provisioning successful!")
        with open("provisioned-certificate.crt", "w") as cert_file:
            cert_file.write(response["certificatePem"])
        with open("provisioned-private.key", "w") as key_file:
            key_file.write(response["keyPair"]["PrivateKey"])
    else:
        print("Provisioning failed!")


# Main Logic
try:
    # Connect to AWS IoT Core
    print("Connecting to AWS IoT Core...")
    mqtt_client.connect()
    print("Connected!")

    # Subscribe to response topic
    mqtt_client.subscribe(RESPONSE_TOPIC, 1, on_provisioning_response)

    # Publish provisioning request
    print("Sending provisioning request...")
    provisioning_payload = {
        "certificateOwnershipToken": "",  # Token obtained during TLS handshake
        "parameters": {"ThingName": THING_NAME, "CustomAttribute": "example-value"},
    }
    mqtt_client.publish(PROVISIONING_TOPIC, json.dumps(provisioning_payload), 1)

    # Wait for response
    time.sleep(10)  # Wait for the response callback

except Exception as e:
    print(f"Error: {e}")

finally:
    mqtt_client.disconnect()
    print("Disconnected.")
