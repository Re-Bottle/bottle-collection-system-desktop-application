import keyring
import requests
from misc.file_handling import save_to_file
from misc.utility import OWNER_ID_NAME, REGISTRATION_SERVICE_NAME, REGISTRATION_STATE, USER_NAME, ApplicationState

SERVER = "http://localhost:3000"  # URL of the server
application_state = ApplicationState

class RegistrationResponse:
    response_code: int = 0
    isRegistered: REGISTRATION_STATE = REGISTRATION_STATE.UNREGISTERED
    owner_id: str = ""

    def __init__(
        self,
        response_code: int,
        isRegistered: REGISTRATION_STATE,
        owner_id: str,
    ):
        self.response_code = response_code
        self.isRegistered = isRegistered
        self.owner_id = owner_id


def ping(device_id: str) -> bool:
    try:
        # Sending a GET request to the server
        response = requests.get(SERVER, params={"id": device_id})

        if response.status_code == 200:
            print("Ping was successful")
            return True
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server")
    return False


def get_registration_status(device_id: str, mac_address: str="00:14:22:01:23:45") -> RegistrationResponse:
    try:
        # Sending a POST request to the server
        response = requests.post(
            SERVER + "/device/register",
            # TODO: Add the device ID and MAC address
            json={"id": device_id, "macAddress": mac_address},
        )
        if response.status_code == 201:
            # Save provisioningDetails.certificateArn, provisioningDetails.certificatePem, provisioningDetails.privateKey to the local system
            provisioningDetails = response.json()
            save_to_file(
                provisioningDetails["certificatePem"], "certificates/ReBottle.cert.pem"
            )
            save_to_file(
                provisioningDetails["keyPair"]["PrivateKey"], "certificates/ReBottle.private.key"
            )
            if (response.json()["deviceState"]) == "Provisioned":
                RegistrationResponse.isRegistered = REGISTRATION_STATE.REGISTERED
                keyring.set_password(REGISTRATION_SERVICE_NAME, USER_NAME, REGISTRATION_STATE.REGISTERED.value)
                keyring.set_password(OWNER_ID_NAME, USER_NAME, response.json()["ownerID"])
            # x={}
               
            return RegistrationResponse(
                response.status_code,
                REGISTRATION_STATE.REGISTERED,
                response.json()["ownerID"],
            )
        else:
            return RegistrationResponse(
                response.status_code, REGISTRATION_STATE.UNREGISTERED, ""
            )

    except requests.exceptions.ConnectionError as e:
        print("Error registering the device: ", e)
        return RegistrationResponse(404, REGISTRATION_STATE.UNREGISTERED, "")
