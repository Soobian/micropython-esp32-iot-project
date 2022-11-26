import time
import network
from umqttsimple import MQTTClient
import json
import configparser


config = configparser.ConfigParser()
config.read('iot-config.ini')

if 'DEFAULT' in config:
    SSID = config['DEFAULT']['SSID']
    PASS = config['DEFAULT']['PASS']
    THING_NAME = config['DEFAULT']['THING_NAME']
    TOPIC = config['DEFAULT']['TOPIC']
    ENDPOINT = config['DEFAULT']['ENDPOINT']
    ROOT_CA = open(config['DEFAULT']['ROOT_CA'], 'r').read()
    CERTIFICATE = open(config['DEFAULT']['CERTIFICATE'], 'r').read()
    PRIVATE_KEY = open(config['DEFAULT']['PRIVATE_KEY'], 'r').read()

SSL_CONFIG  = {'key': PRIVATE_KEY,'cert': CERTIFICATE, 'server_side': False}

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.connect(SSID, PASS)
        while not sta_if.isconnected():
            pass
    print('Connected to network...')
    print('network config:', sta_if.ifconfig())

def message_callback(topic, message):
    print(json.loads(message))

def connect_iot_core():
    mqtt = MQTTClient(
        THING_NAME, 
        ENDPOINT, 
        port = 8883, 
        keepalive = 10000, 
        ssl = True, 
        ssl_params = SSL_CONFIG)
    mqtt.connect()
    mqtt.set_callback(message_callback)
    print('Connected to: {}'.format(ENDPOINT))
    mqtt.subscribe(TOPIC)
    print('Subscribed to topic: {}'.format(TOPIC))
    return mqtt

if __name__ == '__main__':
    connect_wifi()
    subscription = connect_iot_core()
    while True:
        subscription.wait_msg()
        time.sleep(1)