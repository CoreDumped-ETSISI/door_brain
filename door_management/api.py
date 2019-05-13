from rest_framework.views import APIView
from rest_framework.response import Response
from paho.mqtt import client as mqtt
from door_brain.settings import MQTT_SETTINGS, BROKER_DUTIES
from mqtt_brokers.models import Broker
from doors.models import Door
import json


class MqttSendMessageBroadcast(APIView):
    def get(self, request, message):
        brokers = Broker.objects.filter(duty=BROKER_DUTIES.get("MANAGEMENT"))
        error_message = []
        if len(brokers) is 0:
            return Response({'ERROR': 'No Manage brokers registered'}, status=404)
        for broker in brokers:
            try:
                mqtt_manager = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))
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
            mqtt_manager = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))
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


class MqttUpdateDoors(APIView):
    def get(self, request):
        mqtt_manager = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))
        doors = Door.objects.get_queryset()
        if len(doors) is 0:
            return Response({'ERROR': 'Door not found'}, status=404)

        for door in doors:
            mqtt_groups = door.groups.get_queryset()
            cards_to_attach = {}
            groups_to_attach = {}
            for group in mqtt_groups:
                groups_to_attach[group.name] = {
                    'init_date': group.initial_date.strftime('%Y-%m-%d'),
                    'exp_date': group.expiration_date.strftime('%Y-%m-%d'),
                    'time_table': group.get_time_table()
                }
                users = group.user_set.all()
                for user in users:
                    cards = user.card_set.all()
                    for card in cards:
                        card_hash = card.hash
                        if card_hash not in cards_to_attach:
                            cards_to_attach[card_hash] = {
                                'init_date': card.initial_date.strftime('%Y-%m-%d'),
                                'exp_date': card.expiration_date.strftime('%Y-%m-%d'),
                                'groups': []
                            }
                        cards_to_attach[card_hash]['groups'].append(group.name)
            message = json.dumps({
                'groups': groups_to_attach,
                'cards': cards_to_attach
            })
            broker = door.manage_broker
            mqtt_manager.connect(host=broker.ip, port=broker.port)
            mqtt_manager.publish(
                topic=door.manage_topic,
                payload=message
            )
        return Response(status=200)
