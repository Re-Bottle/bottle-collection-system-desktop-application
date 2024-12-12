import requests

from misc.utility import REGISTRATION_STATE

SERVER = "http://localhost:3000"  # URL of the server


class RegistrationResponse:
    response_code: int = 0
    isRegistered: REGISTRATION_STATE = REGISTRATION_STATE.UNREGISTERED
    owner_id: str = ""
    claimed_at: str = ""

    def __init__(
        self,
        response_code: int,
        isRegistered: REGISTRATION_STATE,
        owner_id: str,
        when_claimed: str,
    ):
        self.response_code = response_code
        self.isRegistered = isRegistered
        self.owner_id = owner_id
        self.claimed_at = when_claimed


def ping(device_id: str) -> bool:
    try:
        # Sending a GET request to the server
        response = requests.get(SERVER, params={"deviceID": device_id})

        if response.status_code == 200:
            print("Ping was successful")
            return True
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server")
    return False


def get_registration_status(device_id: str) -> RegistrationResponse:
    try:
        # Sending a POST request to the server
        response = requests.post(
            SERVER + "/device/register", params={"deviceID": device_id}
        )

        if response.status_code == 200:
            return RegistrationResponse(
                response.status_code,
                REGISTRATION_STATE(response.json()["registrationStatus"]),
                response.json()["ownerID"],
                response.json()["whenClaimed"],
            )
        else:
            print("Failed to register device")
            return RegistrationResponse(
                response.status_code, REGISTRATION_STATE.UNREGISTERED, "", ""
            )

    except requests.exceptions.ConnectionError:
        print("Failed to register device")
        return RegistrationResponse(404, REGISTRATION_STATE.UNREGISTERED, "", "")
