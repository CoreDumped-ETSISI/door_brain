from rest_framework.views import APIView
from rest_framework.response import Response
from paho.mqtt import client as mqtt
from door_brain.settings import MQTT_SETTINGS, BROKER_DUTIES
from mqtt_brokers.models import Broker
from doors.models import Door
import json

mqtt_manager = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))


class MqttSendMessageBroadcast(APIView):
    def get(self, request, message):
        brokers = Broker.objects.filter(duty=BROKER_DUTIES.get("MANAGEMENT"))
        error_message = []
        if len(brokers) is 0:
            return Response({'ERROR': 'No Manage brokers registered'}, status=404)
        for broker in brokers:
            try:
                mqtt_manager.connect(host=broker.ip, port=broker.port)
                mqtt_manager.publish(
                    topic=MQTT_SETTINGS.get('TOPICS').get('MANAGEMENT_BROADCAST'),
                    payload=message
                )
            except Exception as err:
                error_message += [{
                    'broker_ip': broker.ip,
                    'ERROR': err.args
                }]
        return Response({
            "Message": 'Message sent',
            "ERRORS": error_message
        }, status=200)


class MqttSendMessageDetail(APIView):
    def get(self, request, door_id, message):
        door_set = Door.objects.filter(id=door_id)
        if len(door_set) is 0:
            return Response({'ERROR': 'Door not found'}, status=404)
        door = door_set[0]
        manage_broker = door.manage_broker
        error_message = []
        try:
            mqtt_manager.connect(host=manage_broker.ip, port=manage_broker.port)
            mqtt_manager.publish(
                topic=door.manage_topic,
                payload=message
            )
        except Exception as err:
            error_message += [{
                'broker_ip': manage_broker.ip,
                'ERROR': err.args
            }]
        return Response({
            "Message": 'Message sent',
            "ERRORS": error_message
        }, status=200)
