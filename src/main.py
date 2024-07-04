import esp
import socket as soc
import camera
from time import sleep

hdr = {
  # live stream -
  # URL: /live
  'stream': """HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=kaki5
Connection: keep-alive
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Expires: Thu, Jan 01 1970 00:00:00 GMT
Pragma: no-cache""",
  # live stream -
  # URL:
  'frame': """--kaki5
Content-Type: image/jpeg"""}

esp.osdebug(None)   # turn off debugging log. Uncomment to show debugging log

UID = const('kohare')  # authentication user
PWD = const('yodare')  # authentication password

cam = camera.init() # Camera
print("Camera ready?: ", cam)

if cam:
    # set preffered camera setting
    camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
    camera.contrast(2)       # increase contrast
    # camera.speffect(2)       # jpeg grayscale

    # TCP server
    port = 80
    addr = soc.getaddrinfo('0.0.0.0', port)[0][-1]
    s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    # s.settimeout(5.0)
    while True:
        cs, ca = s.accept()   # wait for client connect
        print('Request from:', ca)
        w = cs.recv(200) # blocking
        (_, uid, pwd) = w.decode().split('\r\n')[0].split()[1].split('/')
        # print(_, uid, pwd)
        if not (uid==UID and pwd==PWD):
            print('Not authenticated')
            cs.close()
            continue
        # We are authenticated, so continue serving
        cs.write(b'%s\r\n\r\n' % hdr['stream'])
        pic=camera.capture
        put=cs.write
        hr=hdr['frame']
        while True:
            # once connected and authenticated just send the jpg data
            # client use HTTP protocol (not RTSP)
            try:
                put(b'%s\r\n\r\n' % hr)
                put(pic())
                put(b'\r\n')  # send and flush the send buffer
            except Exception as e:
                print('TCP send error', e)
                cs.close()
                break
else:
    print("Camera not ready.")
    print("System not ready. Please restart")

print('System aborted')
