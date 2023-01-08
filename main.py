import time
import network
from umqtt.simple import MQTTClient
import json
import ujson

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('Connected to network...')
    print('network config:', sta_if.ifconfig())

def message_callback(topic, message):
    print(json.loads(message))

def connect_iot_core(name, endpoint, ssl_config):
    mqtt = MQTTClient(
        name, 
        endpoint, 
        port = 8883, 
        keepalive = 10000, 
        ssl = True, 
        ssl_params = ssl_config)
    mqtt.connect()
    mqtt.set_callback(message_callback)
    print('Connected to: {}'.format(endpoint))
    
    return mqtt

if __name__ == '__main__':
    ssid, passoword = "SSID", "PASSWORD"
    with open("config.json", "r") as config:
        parsed = ujson.loads(config.read())
        ssid = parsed["SSID"]
        password = parsed["PASS"]
        thing_name = parsed["THING_NAME"]
        topic = parsed["TOPIC"]
        endpoint = parsed["ENDPOINT"]
        root_ca = open(parsed["ROOT_CA"]).read()
        certificate = open(parsed["CERTIFICATE"]).read()
        private_key = open(parsed["PRIVATE_KEY"]).read()
    

    print(ssid, password)
    connect_wifi(ssid, password)
    
    ssl_config = {'key': private_key,'cert': certificate, 'server_side': False}
    mqtt = connect_iot_core(thing_name, endpoint, ssl_config)

    while True:
        mqtt.publish("ESP32/pub", "Message")
        print('Published topic: {}'.format(topic))
        time.sleep(1)