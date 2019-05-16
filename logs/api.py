from rest_framework.generics import ListAPIView
from logs.models import Log
from rest_framework.views import APIView
from rest_framework.response import Response
from paho.mqtt import client as mqtt
from door_brain.settings import MQTT_SETTINGS, BROKER_DUTIES
from mqtt_brokers.models import Broker
from logs.serializers import MqttLogsListenerSerial
import json

mqtt_clients = []


class LogsView(ListAPIView):
    queryset = Log.objects.all()
    serializer_class = MqttLogsListenerSerial


class MqttConnectView(APIView):
    def get(self, request):
        global mqtt_clients
        success_message = []
        error_message = []
        brokers = Broker.objects.filter(duty=BROKER_DUTIES.get("LOGS"))
        if len(brokers) is 0:
            return Response({'ERRORS': 'No brokers registered'}, status=404)
        for old_client in mqtt_clients:
            old_client.disconnect()
            del old_client
        mqtt_clients = []
        for broker in brokers:
            try:
                mqtt_clients = []
                mqtt_client = mqtt.Client()
                mqtt_client.connect(host=broker.ip, port=broker.port)
                mqtt_client.subscribe(topic=MQTT_SETTINGS.get("TOPICS").get("LOGS"))
                mqtt_client.on_message = lambda client, userdata, message: self.createLog(message)
                mqtt_client.loop_start()
                mqtt_clients.append(mqtt_client)
                success_message.append('Mqtt connection with broker ' + broker.ip + ' success')
            except Exception as err:
                error_message += [{
                    'broker_ip': broker.ip,
                    'ERROR': err.args
                }]
        return Response({
            "SUCCESS": success_message,
            "ERRORS": error_message
        }, status=200)

    def createLog(self, m):
        data = json.loads(m.payload)
        serializer = MqttLogsListenerSerial(data=data)
        if serializer.is_valid():
            serializer.create(validated_data=serializer.validated_data)
        else:
            print(serializer.errors)
