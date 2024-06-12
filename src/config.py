app_config = {
    'sleep-ms': 2000,
    'max-error': 10,
    'ftp': False,
    'mode': 'microSD', # mode -> 'MQTT' or 'microSD'
    'camera': 'ESP32-CAM',  # camera -> 'ESP32-CAM' or 'M5CAMERA'
    'led': 21
}

# mqtt_config = {
#     'server': '192.168.178.147',
#     'client_id': 'esp32-camera',
#     'topic': b'Image'
# }

microsd_config = {
    'miso':2,
    'mosi':15,
    'ss':13,
    'sck':14,
}

wifi_config = {
    'ssid':'',
    'password':''
}

slack_config = {
    'hook_url': ''
}
