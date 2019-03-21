from django.urls import path
from logs.api import LogsView

base_url = 'logs/'

urlpatterns = [
    path(base_url, LogsView.as_view(), name="list_logs")
]
