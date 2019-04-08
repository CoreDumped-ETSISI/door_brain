from rest_framework.views import APIView
from rest_framework.response import Response
from paho.mqtt import client as mqtt
from door_brain.settings import MQTT_SETTINGS
from mqtt_brokers.models import Broker
from logs.serializers import MqttLogsListenerSerial

mqtt_manager = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))


class MqttConnectView(APIView):
    def get(self, request):
        success_message = []
        error_message = []
        brokers = Broker.objects.all()
        if len(brokers) is 0:
            return Response({'ERRORS': 'No brokers registered'}, status=404)
        for broker in brokers:
            try:
                mqtt_client = mqtt.Client(client_id=MQTT_SETTINGS.get("CLIENT_ID"))
                mqtt_client.connect(host=broker.ip)
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
        data = {
            'message': m.payload.decode('utf-8')
        }
        serializer = MqttLogsListenerSerial(data=data)
        if serializer.is_valid():
            serializer.create(validated_data=serializer.validated_data)
        else:
            print(serializer.errors)


class MqttSendMessage(APIView):
    def get(self, request, message):
        brokers = Broker.objects.filter(duty="management")
        error_message = []
        for broker in brokers:
            try:
                print(broker.ip)
                mqtt_manager.connect(broker.ip)
                mqtt_manager.publish(
                    topic=MQTT_SETTINGS.get('TOPICS').get('MANAGEMENT'),
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
