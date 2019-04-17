from django.urls import path
from door_management.api import MqttSendMessage

base_url = 'manage/'

urlpatterns = [
    path(base_url + 'sendMessage/<str:message>', MqttSendMessage.as_view(), name="mqtt_send_message")
]
