from django.urls import path
from mqtt_brokers.api import MqttConnectView

base_url = 'mqtt/'

urlpatterns = [
    path(base_url + 'listenLogs', MqttConnectView.as_view(), name="mqtt_logs")
]
