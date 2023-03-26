import logging
import os
import socket
import time
import subprocess
import re
from typing import Dict, Tuple

from roonapi import RoonApi, RoonDiscovery

CHECK_INTERVAL = 1
ZONE_NAME = 'hqplayer'

appinfo = {
    "extension_id": "Roon_Screen_Control",
    "display_name": "Dashboard Screen Control for Roon",
    "display_version": "1.0.0",
    "publisher": "jimmytheshoebill",
    "email": "",
}

# Define the host and wait time variables
HOST = "<redacted for privacy>"
WAIT_TIME = 30

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def set_display_id():
    """
    Set the display ID.
    """
    cmd = "ps aux | grep 'Xorg'"
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, text=True)
    xorg_processes = result.stdout.strip().split("\n")

    display_ids = []
    for process in xorg_processes:
        match = re.search(r'(?<=tcp ).*?(?= vt)', process)
        if match:
            display_ids.append(match.group())
    if len(display_ids) > 0:
        logging.info(f"Setting display ID to {display_ids[0]}")
        os.environ['DISPLAY'] = display_ids[0] + '.0'

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

def is_host_reachable(host: str, port: int = 9330, timeout: int = 5) -> bool:
    """
    Check if a host is reachable.

    :param host: Hostname or IP address of the host
    :param port: Port number to check (default: 9330)
    :param timeout: Timeout in seconds for the connection attempt (default: 5)
    :return: True if the host is reachable, False otherwise
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(f"Error: {ex}")
        return False

def on_error():
    """
    Handle WebSocket errors.
    """
    os.system("sudo pkill -KILL -u admin -t tty1")

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
    time.sleep(5)
    core_id, token = read_files("my_core_id_file", "my_token_file")
    server = discover_roon(core_id)
    roonapi = connect_roon(appinfo, token, server)

    while True:
        if is_host_reachable(HOST):
            set_display_id()
            toggle_display(roonapi, ZONE_NAME)
        else:
            logging.info(f"Host '{HOST}' is not reachable. Waiting for {WAIT_TIME} seconds...")
            time.sleep(WAIT_TIME)
            on_error()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
