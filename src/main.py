import uos
import machine
import gc
import ntptime
import time
import camera
from config import *
from slack import Slack
from mqtt import Mqtt

slack_client = Slack()
mqtt_client = Mqtt()

try:
    # camera init
    led = machine.Pin(app_config['led'], machine.Pin.OUT)

    if app_config['camera'] == 'ESP32-CAM':
        # camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)  # ESP32-CAM
        camera.init()  # From https://wiki.seeedstudio.com/XIAO_ESP32S3_Micropython/
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
    elif app_config['mode'] == 'MQTT':
        mqtt_client.start()

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
        print("Initial free memory:", gc.mem_free())
        print("Initial allocated memory:", gc.mem_alloc())

        # prepare for photo
        led.value(1)
        led.value(0)

        # take photo
        buf = camera.capture()
        # save photo
        timestamp = rtc.datetime()
        time_str = '%4d%02d%02d%02d%02d%02d' %(timestamp[0], timestamp[1], timestamp[2], timestamp[4], timestamp[5], timestamp[6])

        print(f'Took photo {time_str}: {buf[:20]}')
        print("After allocation free memory:", gc.mem_free())
        print("After allocation allocated memory:", gc.mem_alloc())

        if app_config['mode'] == 'microSD':
            f = open('sd/'+time_str+'.jpg', 'w')
            f.write(buf)
            time.sleep_ms(100)
            f.close()
        elif  app_config['mode'] == 'MQTT':
            mqtt_client.publish(mqtt_config['topic'], buf)

        print(f'Saved photo {time_str}: {buf[:20]}')

        del buf
        gc.collect()
        print("After gc.collect() free memory:", gc.mem_free())
        print("After gc.collect() allocated memory:", gc.mem_alloc())

        # sleep
        time.sleep_ms(app_config['sleep-ms'])

    except KeyboardInterrupt:
        mqtt_client.stop()
        print("debugging stopped")
        loop = False

    except Exception as e:
        print("Error ocurred: " + str(e))
        error_counter = error_counter + 1
        if error_counter > app_config['max-error']:
            machine.reset()
