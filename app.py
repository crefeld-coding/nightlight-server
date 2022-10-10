import json
import time

import paho.mqtt.client as mqtt

#id = '14147f4e-7ba3-4e86-ac81-f5d61470903e'
id = '1e0acfc6-1f47-4ff9-aba7-4300f6b9fa71'

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
