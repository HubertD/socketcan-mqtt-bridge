#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.loop_start()

while True:
	client.publish('can/vcan0/send', payload=json.dumps({'id':0x123, 'd':[1,2,3,4]}), qos=0, retain=False)
	time.sleep(0.1)

	client.publish('can/vcan0/send', payload=json.dumps({'id':0x123, 'ext':True}), qos=0, retain=False)
	time.sleep(0.1)

