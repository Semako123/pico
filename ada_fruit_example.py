import network
import socket
from time import sleep
import ahtx0
from machine import Pin, I2C
from umqtt.simple import MQTTClient
import random


import wificonnect
print("Connected to Wifi.")

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)

mqtt_server = 'io.adafruit.com'
mqtt_port = 1883 # non-SSL port
mqtt_user = 'semako123' #Adafruit ID
mqtt_password = 'aio_euZi80v6kBkkNu9o6eFhz1aD886X' # Under Keys
mqtt_topic = 'semako123/feeds/study_temp' # Under "Feed info"
mqtt_client_id = str(random.randint(10000,999999)) #must have a unique ID - good enough for now

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)

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
    
while True:
    if wlan.isconnected():
        client.publish(mqtt_topic, str(sensor.temperature))
    else:
        reconnect()
    sleep(20)