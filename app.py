import json
import time

import paho.mqtt.client as mqtt

id_ff = '14147f4e-7ba3-4e86-ac81-f5d61470903e'
id = '1e0acfc6-1f47-4ff9-aba7-4300f6b9fa71'
id_es = '366b0063-326c-4751-a6c6-a538017ad105'
id_lw = '775f8bc0-4d05-406b-b6e2-a0d9c1f29cd2'
id_ss = '4b5b2bdf-25e6-4c7b-8ce7-aa79cfa3c606'
id_zh = '76822185-e8c8-42dc-8757-7def6b3882b5'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_server'

old_led_state = False

print("Making client")
mqtt_client = mqtt.Client(client_name)
print("Connecting")
mqtt_client.connect('test.mosquitto.org')

print("Loop start")
mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    global old_led_state
    print("Handling msg!")
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    new_led_state = payload['light'] < 300

    if (new_led_state != old_led_state):
        old_led_state = new_led_state
        command = { 'led_on' : payload['light'] < 300 }
        print("Sending message:", command)

        client.publish(server_command_topic, json.dumps(command))

print("Subscribing")
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    print("Loop and wait.")
    time.sleep(5)
