import coreapi
import coreschema

base_url = '/manage/'

BroadcastSchema = coreapi.Link(
    url=base_url+'sendMessage/{message}',
    action='get',
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
    url=base_url+'sendMessage/{door_id}/{message}',
    action='get',
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
