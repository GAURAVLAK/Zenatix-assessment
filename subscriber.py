# python 3.6

import json
import random
import time

from paho.mqtt import client as mqtt_client

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "3acekl7197/"
CLIENT_ID = f'subscribe-1'
USERNAME = '3acekl7197'
PASSWORD = '3578hmouvz'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60
CONSECUTIVE_READINGS = 5
THRESHOLD = 25
FLAG_EXIT = False

recent_readings = []
def check_threshold(reading):
    global recent_readings
    recent_readings.append(reading)

    if len(recent_readings) > CONSECUTIVE_READINGS:
        recent_readings.pop(0)

    if len(recent_readings) == CONSECUTIVE_READINGS and all(r > THRESHOLD for r in recent_readings):
        return True
    return False

def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f'Failed to connect, return code {rc}')


def on_disconnect(client, userdata, rc):
    if client.is_connected():
        print("Client connected")
    else :
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            time.sleep(reconnect_delay)

        try:
            print("inside disconnect trying to reconnect")
            client.reconnect()
            return
        except Exception as err:

            reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    global FLAG_EXIT
    FLAG_EXIT = True


def on_message(client, userdata, msg):
    print('Inside on_message')
    print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')
    a = (msg.payload.decode())
    data = json.loads(a)

    temp_value = float(data['Temp'])
    if check_threshold(temp_value):
        print("ALARM! sensor value has crossed the threshold continuously for 5 minutes.")
    with open('timestamp.txt','a') as file:
        file.write(a+ '\n')

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    client.on_disconnect = on_disconnect
    return client



def run():
    print("Inside run")
    client = connect_mqtt()
    while(1):
        client.loop_start()
        time.sleep(1)

    if client.is_connected():
        print("Client connected")
    else:
        client.loop_stop()


if __name__ == '__main__':
    run()
