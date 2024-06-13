import uos
import machine

import ntptime
import time
import camera
from config import *
from slack import Slack

slack_client = Slack()

if  app_config['mode'] == 'MQTT':
    from umqtt.simple2 import MQTTClient

try:
    # camera init
    led = machine.Pin(app_config['led'], machine.Pin.OUT)

    if app_config['camera'] == 'ESP32-CAM':
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)  # ESP32-CAM
    elif app_config['camera'] == 'M5CAMERA':
        camera.init(0, d0=32, d1=35, d2=34, d3=5, d4=39, d5=18, d6=36, d7=19,
                    href=26, vsync=25, reset=15, sioc=23, siod=22, xclk=27, pclk=21, fb_location=camera.PSRAM)   #M5CAMERA

    if app_config['mode'] == 'microSD':
        # sd mount
        sd = machine.SDCard(slot=3, width=1,
                            sck=machine.Pin(microsd_config['sck']),
                            mosi=machine.Pin(microsd_config['mosi']),
                            miso=machine.Pin(microsd_config['miso']),
                            cs=machine.Pin(microsd_config['ss']))
        uos.mount(sd, '/sd')
        #uos.listdir('/')
    elif  app_config['mode'] == 'MQTT':
        c = MQTTClient(mqtt_config['client_id'], mqtt_config['server'])
        c.connect()

    # ntp sync for date
    ntptime.settime()
    rtc = machine.RTC()

except Exception as e:
    print("Error ocurred: " + str(e))
    time.sleep_ms(5000)
    machine.reset()

error_counter = 0
loop = True
while loop:
    try:
        # prepare for photo
        led.value(1)
        led.value(0)

        # take photo
        buf = camera.capture()
        # save photo
        timestamp = rtc.datetime()
        time_str = '%4d%02d%02d%02d%02d%02d' %(timestamp[0], timestamp[1], timestamp[2], timestamp[4], timestamp[5], timestamp[6])

        slack_client.send_message(f'Took photo {time_str}')

        if app_config['mode'] == 'microSD':
            f = open('sd/'+time_str+'.jpg', 'w')
            f.write(buf)
            time.sleep_ms(100)
            f.close()
        elif  app_config['mode'] == 'MQTT':
            c.publish(mqtt_config['topic'], buf)

        slack_client.send_message(f'Saved photo {time_str}')

        # sleep
        time.sleep_ms(app_config['sleep-ms'])

    except KeyboardInterrupt:
        print("debugging stopped")
        loop = False

    except Exception as e:
        print("Error ocurred: " + str(e))
        error_counter = error_counter + 1
        if error_counter > app_config['max-error']:
            machine.reset()
