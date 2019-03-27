from django.urls import path
from mqtt_brokers.api import MqttConnectView, MqttSendMessage

base_url = 'mqtt/'

urlpatterns = [
    path(base_url + 'listenLogs', MqttConnectView.as_view(), name="mqtt_logs"),
    path(base_url + 'sendMessage/<str:message>', MqttSendMessage.as_view(), name="mqtt_send_message")
]
