from rest_framework import serializers
from logs.models import Log


class MqttLogsListenerSerial(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
