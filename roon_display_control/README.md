# Roon Screen Control

Roon Screen Control is a Python script that toggles the display on and off based on the playback status of a specified Roon zone. The script runs as a daemon process and checks the status of the zone every 1 second.

The script is tested on Raspberry Pi 4 connecting with an external HDMI display as a Roon display.

## Requirements

- Python 3.6 or higher
- Roon API: Install it using `pip install roonapi`
- You have setup your device as a web kiosk pointing to Roon display URL with browser such as Chromium.

## Setup

1. Clone the repository or download the Python script `display_control.py`.
2. In the same directory as the script, create two files: `my_core_id_file` and `my_token_file`. These files should contain your Roon core_id and API token, respectively.
3. Make sure your system has the `xset` command installed. This command is used to control the display.

## Usage

Run the script using the following command:

```
python3 display_control.py
```

The script will run as a daemon process and check the playback status of the specified Roon zone every second. If the status is not 'playing', the display will be turned off. Otherwise, the display will be turned on.

## Customization
To change the target zone name, edit the following line in the display_control.py file:
```
ZONE_NAME = 'hqplayer'
```
Replace 'hqplayer' with the desired zone name.

To change the desired check intervals to Roon Server, change this line:
```
CHECK_INTERVAL = 1
```

## Systemd service (Optional)
Use the non-daemonized script if you plan to use systemd to run the script. Otherwise double-fock will occur.

To automatically run the script at startup on a Debian-based system, follow these steps:

Create a systemd service file:
sudo nano /etc/systemd/system/roon_screen_control.service

Add the following content to the file, replacing the path to the script with the actual path on your system:
```
[Unit]
Description=Roon Screen Control
After=network.target

[Service]
User=admin
Group=admin
Type=simple
ExecStart=/usr/bin/python3 /path/to/your/display_control.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Make sure to replace /path/to/your/display_control.py with the actual path to the Python script.

Save the file and exit the text editor.
Reload the systemd manager configuration:
```
sudo systemctl daemon-reload
```
Enable the service to start on boot:
```
sudo systemctl enable roon_screen_control.service
```
Start the service:
```
sudo systemctl start roon_screen_control.service
sudo systemctl status roon_screen_control.service
```

Now, the script will run as the admin user on system boot.

## Enhanced version to handle Roon reboots (display_control_enhanced.py)
This enhanced version of the script handles Roon server reboots, reloads Xorg and Chromium, and retries the connection to the Roon server.

## Features

- Checks if the Roon server is reachable.
- Handles Roon server reboots.
- Reloads Xorg and Chromium when needed.
- Retries the connection to the Roon server.

## Configuration

- `CHECK_INTERVAL`: The time interval (in seconds) to wait between checking the Roon zone's status. (Default: 1 second)
- `ZONE_NAME`: The name of the Roon zone to monitor. (Default: 'hqplayer')
- `HOST`: The hostname or IP address of the Roon server to check for reachability.
- `WAIT_TIME`: The time interval (in seconds) to wait before retrying the connection to the Roon server. (Default: 30 seconds)
