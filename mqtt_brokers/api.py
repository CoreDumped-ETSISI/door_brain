from rest_framework.views import APIView
from rest_framework.response import Response
from paho.mqtt import client as mqtt
from door_brain.settings import MQTT_SETTINGS
from mqtt_brokers.models import Broker
from logs.serializers import MqttLogsListenerSerial

mqtt_manager = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))


def createLog(m):
    data = {
        'message': m.payload.decode('utf-8')
    }
    serializer = MqttLogsListenerSerial(data=data)
    if serializer.is_valid():
        serializer.create(validated_data=serializer.validated_data)
    else:
        print(serializer.errors)


class MqttConnectView(APIView):
    def get(self, request):
        for broker in Broker.objects.all():
            mqtt_client = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))
            mqtt_client.connect(host=broker.ip)
            mqtt_client.subscribe(topic=MQTT_SETTINGS.get("TOPICS").get("LOGS"))
            mqtt_client.on_message = lambda client, userdata, message: createLog(message)
            mqtt_client.loop_start()

        return Response({"message": "mqtt connection success"}, status=200)
