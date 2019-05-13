import coreapi
from logs.urls import base_url

ListLogs = coreapi.Link(
    url='/'+base_url,
    action='get',
    description='Return all logs'
)

LogsListener = coreapi.Link(
    url='/'+base_url+'listenLogs',
    action='get',
    description='Set up mqtt clients to start listen the door\'s logs'
)
