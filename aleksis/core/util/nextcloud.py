from typing import Union

import requests
from constance import config

HEADERS = {
    "User-Agent": "AlekSIS",
}
INITIATE_LOGIN_PROCESS_URL = "index.php/login/v2"


def initiate_login_process(nextcloud_url: str) -> dict:
    url = nextcloud_url + INITIATE_LOGIN_PROCESS_URL

    r = requests.post(url, headers=HEADERS)

    return r.json()


def login_process_poll(endpoint: str, token: str) -> Union[dict, bool]:
    r = requests.post(endpoint, headers=HEADERS, data={"token": token})

    if r.status_code != 200:
        return False

    return r.json()


def is_connected() -> bool:
    return (
        config.NEXTCLOUD_TALK_SERVER != ""
        and config.NEXTCLOUD_TALK_LOGIN_NAME != ""
        and config.NEXTCLOUD_TALK_APP_PASSWORD
    )
