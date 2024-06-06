from machine import Pin
from hcsr04 import HCSR04
from time import sleep

sensor = HCSR04(trigger_pin=15, echo_pin=14)
led1 = Pin(12, Pin.OUT)
led2 = Pin(13, Pin.OUT)

while True:
    distance = sensor.distance_cm()
    print("Distance: ", distance, "cm")
    
    if distance > 10:
        led2.on()
        led1.off()
    else:
        led1.on()
        led2.off()
        
    sleep(0.25)



