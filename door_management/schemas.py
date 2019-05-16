import coreapi
import coreschema
from door_management.urls import base_url


BroadcastSchema = coreapi.Link(
    url='/'+base_url+'sendMessage/{message}',
    action='get',
    description='Send a message to all doors',
    fields=[
        coreapi.Field(
            name='message',
            required=True,
            location='path',
            description='Message to send in broadcast',
            schema=coreschema.String(),
        ),
    ]
)

DetailSchema = coreapi.Link(
    url='/'+base_url+'sendMessage/{door_id}/{message}',
    action='get',
    description='Send a message to a specific door',
    fields=[
        coreapi.Field(
            name='door_id',
            required=True,
            location='path',
            description='Door which send message',
            schema=coreschema.String()
        ),
        coreapi.Field(
            name='message',
            required=True,
            location='path',
            description='Message to send',
            schema=coreschema.String()
        ),
    ]
)

UpdateDoors = coreapi.Link(
    url='/'+base_url+'updateDoors',
    action='get',
    description='Update door with users cards'
)
