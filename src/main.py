import network
import urequests
import time
from machine import Pin
led_pin = 21  # Default on-board RGB LED GPIO48 does not work

def blink(num):
    led = Pin(led_pin, Pin.OUT)

    for i in range(num):
        led.on()
        time.sleep_ms(500)
        led.off()
    print("Blink")

def wifi_connect(ssid, pwd):
    """
    Connect to a wifi 'ssid' with password 'pwd'
    """

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    return 'IP address: %s' % sta_if.ifconfig()[0]

def to_slack(slack_hook_url, slack_message):
    """
    Send the 'slack_message' using an incoming webhook
    """
    data = {
            "link_names": 1,
            "icon_url": ":ghost:",
            "username": "ESP32S3",
            "text": slack_message
           }
    res = urequests.post(slack_hook_url, json=data)
    return res.status_code == 200

if __name__ == "__main__":
    SSID = ""
    pwd = ""
    slack_hook_url = ""
    slack_message = "Hello from ESP32S3"

    wifi_connect(SSID, pwd)

    ok = to_slack(slack_hook_url, slack_message)
    if ok:
        print("Succeded posting to Slack")
        blink(num=1)
    else:
        print("Failed trying to post to Slack")
        blink(num=3)
