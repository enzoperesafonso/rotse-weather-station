from machine import Pin
import utime

hall_pin = Pin(2, Pin.IN, Pin.PULL_UP)

print("Monitoring Hall sensor on GP15... Bring a magnet near!")

while True:
    if hall_pin.value() == 0:
        print("Magnet detected!")
    else:
        print("No magnet")
    utime.sleep(0.2)
