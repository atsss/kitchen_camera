# Kitchen Camera
## Your settings
- Create `config.py` file and locate it under `src` directory
```
app_config = {
    'sleep-ms': 2000,
    'max-error': 10,
    'ftp': False,
    'mode': 'microSD', # mode -> 'MQTT' or 'microSD'
    'camera': 'ESP32-CAM',  # camera -> 'ESP32-CAM' or 'M5CAMERA'
    'led': 21
}

mqtt_config = {
    'server': '',
    'port':
    'username': '',
    'password': ''
    'topic': b'Image'
}

microsd_config = {
    'miso': 8,
    'mosi': 9,
    'ss': 21,
    'sck': 7,
}

wifi_config = {
    'ssid': '',
    'password': ''
}

slack_config = {
    'hook_url': ''
}
```
