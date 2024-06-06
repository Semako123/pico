from machine import Pin, I2C, Timer
from time import sleep
import ahtx0
from hcsr04 import HCSR04
import network
import socket
from umqtt.simple import MQTTClient
import random

import wificonnect
print("Connected to Wifi.")

mqtt_server = 'io.adafruit.com'
mqtt_port = 1883 # non-SSL port
mqtt_user = 'semako123' #Adafruit ID
mqtt_password = 'aio_euZi80v6kBkkNu9o6eFhz1aD886X' # Under Keys
mqtt_topic1 = 'semako123/feeds/study_temp' # Under "Feed info"
mqtt_topic2 = 'semako123/feeds/reg' # Under "Feed info"
mqtt_topic3 = 'semako123/feeds/cold' # Under "Feed info"
mqtt_topic4 = 'semako123/feeds/hot' # Under "Feed info"
mqtt_client_id = str(random.randint(10000,999999)) #must have a unique ID - good enough for nows

wlan = network.WLAN(network.STA_IF)

def mqtt_connect():
    client = MQTTClient(client_id=mqtt_client_id, server=mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    sleep(5)
    reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)
sensor2 = HCSR04(trigger_pin=8, echo_pin=7)

hot_led = Pin(2, Pin.OUT)
cold_led = Pin(4, Pin.OUT)
reg_led = Pin(3, Pin.OUT)
distance_led = Pin(6, Pin.OUT)

data = distance_led.value()

button = Pin(5, Pin.IN, Pin.PULL_DOWN)

hot_led.off()
cold_led.off()
reg_led.off()

def blink_hot():
    hot_led.on()
    
def blink_cold():
    cold_led.on()

def mqtt_publish_state(timer):
    if wlan.isconnected():
        client.publish(mqtt_topic1, str(distance_led.value()))
        client.publish(mqtt_topic2, str(reg_led.value()))
        client.publish(mqtt_topic3, str(cold_led.value()))
        client.publish(mqtt_topic4, str(hot_led.value()))        
    else:
        reconnect()
        
# Setup a timer to publish temperature every 5 seconds
temp_timer = Timer(-1)
temp_timer.init(period=5000, mode=Timer.PERIODIC, callback=mqtt_publish_state)

while True:
    distance = sensor2.distance_cm()
    
    if distance < 9:
        print("Do not disturb!!!")
        distance_led.on()
    else:
        print("No presence detected")
        distance_led.off()
        
    if button.value():
        print("Button Pressed, Regulate Temperature")
        reg_led.on()
        hot_led.off()
        cold_led.off()
        sleep(10)
    elif sensor.temperature > 27:
        blink_hot()
        reg_led.off()
        cold_led.off()
    elif sensor.temperature < 26.1:
        blink_cold()
        hot_led.off()
        reg_led.off()
    else:
        reg_led.on()
        hot_led.off()
        cold_led.off()
    
    sleep(0.5)
    
