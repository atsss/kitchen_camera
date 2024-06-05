from machine import Pin
import time
led_pin = 21  # Default on-board RGB LED GPIO48 does not work

def blink():
    led = Pin(led_pin, Pin.OUT)
    for i in range(10):
      led.on()
      time.sleep_ms(500)
      led.off()
      time.sleep_ms(500)
      print("Blink ", i+1)

if __name__ == "__main__":
    blink()
