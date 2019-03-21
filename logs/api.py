from rest_framework.generics import ListAPIView
from logs.serializers import MqttLogsListenerSerial
from logs.models import Log


class LogsView(ListAPIView):
        queryset = Log.objects.all()
        serializer_class = MqttLogsListenerSerial
