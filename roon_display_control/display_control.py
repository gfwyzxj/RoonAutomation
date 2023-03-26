import os
import sys
import time
from typing import Dict, Tuple

from roonapi import RoonApi, RoonDiscovery

os.environ['DISPLAY'] = ':0.0'
CHECK_INTERVAL = 1
ZONE_NAME = 'hqplayer'

appinfo = {
    "extension_id": "Roon_Screen_Control",
    "display_name": "Dashboard Screen Control for Roon",
    "display_version": "1.0.0",
    "publisher": "jimmytheshoebill",
    "email": "",
}


def read_files(core_id_file: str, token_file: str) -> Tuple[str, str]:
    """
    Read the core_id and token from their respective files.

    :param core_id_file: The filename of the core_id file.
    :param token_file: The filename of the token file.
    :return: A tuple containing the core_id and token.
    """
    try:
        core_id = open(core_id_file).read()
        token = open(token_file).read()
    except OSError:
        print("Please authorise first using discovery.py")
        exit()

    return core_id, token


def discover_roon(core_id: str) -> Tuple[str, int]:
    """
    Discover the Roon core.

    :param core_id: The core_id of the Roon core.
    :return: A tuple containing the server address and port.
    """
    discover = RoonDiscovery(core_id)
    server = discover.first()
    discover.stop()

    return server[0], server[1]


def connect_roon(appinfo: Dict, token: str, server: Tuple[str, int]) -> RoonApi:
    """
    Connect to the Roon API.

    :param appinfo: A dictionary containing the app information.
    :param token: The Roon API token.
    :param server: A tuple containing the server address and port.
    :return: A RoonApi object.
    """
    return RoonApi(appinfo, token, server[0], server[1], True)


def toggle_display(roonapi: RoonApi, target_display_name: str):
    """
    Toggle the display based on the zone status.

    :param roonapi: A RoonApi object.
    :param target_display_name: The target display name to check the status.
    """
    zones: Dict[str, str] = roonapi.zones
    for item in zones:
        zone = zones.get(item)
        if zone.get('display_name') == target_display_name:
            if zone.get('state') != 'playing':
                os.system('xset dpms force off')
            else:
                os.system('xset dpms force on')


def main():
    """
    Run the main functionality.
    """
    core_id, token = read_files("my_core_id_file", "my_token_file")
    server = discover_roon(core_id)
    roonapi = connect_roon(appinfo, token, server)

    while True:
        toggle_display(roonapi, ZONE_NAME)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
