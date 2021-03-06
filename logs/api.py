from rest_framework.generics import ListAPIView
from logs.models import Log
from rest_framework.views import APIView
from rest_framework.response import Response
from door_brain.utils.mqtt import Mqtt
from door_brain.settings import MQTT_SETTINGS, BROKER_DUTIES
from mqtt_brokers.models import Broker
from logs.serializers import MqttLogsListenerSerial
import json


class LogsView(ListAPIView):
    queryset = Log.objects.all()
    serializer_class = MqttLogsListenerSerial


class MqttConnectView(APIView):
    def get(self, request):
        success_message = []
        error_message = []
        brokers = Broker.objects.filter(duty=BROKER_DUTIES.get("LOGS"))
        if len(brokers) is 0:
            return Response({'ERRORS': 'No brokers registered'}, status=404)

        mqtt_manager = Mqtt.get_manager()
        mqtt_manager.del_clients()
        for broker in brokers:
            mqtt_client = mqtt_manager.get_client()
            try:
                mqtt_client.connect(host=broker.ip, port=broker.port)
                mqtt_client.subscribe(topic=MQTT_SETTINGS.get("TOPICS").get("LOGS"))
                mqtt_client.on_message = lambda client, userdata, message: self.createLog(message)
                mqtt_client.loop_start()
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
