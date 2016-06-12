import paho.mqtt.client as mqtt
import can
import json

can_bustype = 'socketcan_ctypes'
can_channel = 'vcan0'
mqtt_host   = 'localhost'
mqtt_port   = 1883

bus = can.interface.Bus(channel=can_channel, bustype=can_bustype)


def mqtt_on_connect(client, userdata, flags, rc):
	client.subscribe('can/' + can_channel + '/send')


def mqtt_on_message(client, userdata, msg):

	try:
		jmsg = json.loads(msg.payload)
		canmsg = can.Message(
			arbitration_id = jmsg['id'], 
			extended_id = ('ext' in jmsg) and (jmsg['ext'] == True),
			data = jmsg['d'] if 'd' in jmsg else []
		)
		if 'rtr' in jmsg:
			canmsg.is_remote_frame = jmsg['rtr'] == True

		bus.send(canmsg)

	except:
		pass

	
client = mqtt.Client()
client.on_connect = mqtt_on_connect
client.on_message = mqtt_on_message
client.connect(host=mqtt_host, port=mqtt_port, keepalive=60)
client.loop_start()

for msg in bus:

	data = {
		'ts': msg.timestamp,
		'id': msg.arbitration_id
	}

	if (msg.id_type):
		data['ext'] = True
	if (msg.is_remote_frame):
		data['rtr'] = True
	if len(msg.data)>0:
		data['d'] = [i for i in msg.data]
	
	topic = 'can/%s/' + ('%08X' if msg.id_type else '%03X')
	topic = topic % (can_channel, msg.arbitration_id)
	client.publish(topic, payload=json.dumps(data), qos=0, retain=False)

