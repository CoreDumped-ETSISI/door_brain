from django.urls import path
from door_management.api import MqttSendMessageBroadcast, MqttSendMessageDetail

base_url = 'manage/'

urlpatterns = [
    path(base_url + 'sendMessage/<str:message>', MqttSendMessageBroadcast.as_view(), name="mqtt_send_message_broadcast"),
    path(base_url + 'sendMessage/<str:door_id>/<str:message>', MqttSendMessageDetail.as_view(), name="mqtt_send_message_detail")
    # path(base_url + "updateUsers", SomeView.as_view())
]
