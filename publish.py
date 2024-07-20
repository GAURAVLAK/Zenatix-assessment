# python 3.6

import json
import random
import time

from paho.mqtt import client as mqtt_client

#BROKER = 'broker.emqx.io'
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "3acekl7197/"
# generate client ID with pub prefix randomly
#CLIENT_ID = f'python-3acekl7197-pub-sub-{random.randint(0, 1000)}'
CLIENT_ID = f'publish-1'
USERNAME = '3acekl7197'
PASSWORD = '3578hmouvz'

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

FLAG_EXIT = False


def on_connect(client, userdata, flags, rc):
    if rc == 0 and client.is_connected():
        print("Connected to MQTT Broker!")
    else:
        print(f'Failed to connect, return code {rc}')


def on_disconnect(client, userdata, rc):
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            print("Reconnected successfully!")
            return
        except Exception as err:
            print("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    global FLAG_EXIT
    FLAG_EXIT = True

def read_Temperature():
    return round(random.uniform(25,30.3),2)

def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT, keepalive=120)
    client.on_disconnect = on_disconnect
    return client


def publish(client):
    msg_count = 0
    while not FLAG_EXIT:
        timestamp = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime())
        print(time.localtime())
        print(timestamp)
        msg_dict = {
                'Temp': read_Temperature(),
                'timestamp': timestamp
                }
        msg = json.dumps(msg_dict)

        if not client.is_connected():
            time.sleep(1)
            continue
        result = client.publish(TOPIC, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f'Send `{msg}` to topic `{TOPIC}`')
        else:
            print(f'Failed to send message to topic {TOPIC}')
        msg_count += 1
        time.sleep(60)


def run():
    client = connect_mqtt()
    client.loop_start()
    time.sleep(1)
    if client.is_connected():
        publish(client)
    else:
        client.loop_stop()


if __name__ == '__main__':
    run()
