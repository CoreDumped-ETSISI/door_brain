from django.urls import path
from logs.api import LogsView, MqttConnectView

base_url = 'logs/'

urlpatterns = [
    path(base_url, LogsView.as_view(), name="list_logs"),
    path(base_url + 'listenLogs', MqttConnectView.as_view(), name="mqtt_logs"),
]
