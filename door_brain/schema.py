from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from door_management.schemas import BroadcastSchema, DetailSchema, UpdateDoors
from logs.schemas import ListLogs, LogsListener
import coreapi


class SwaggerSchemaView(APIView):
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]
    unprotected_links = {}
    protected_links = {
        'management': {
            'Send Message Broadcast': BroadcastSchema,
            'Send Message Detail': DetailSchema,
            'Update Doors': UpdateDoors
        },
        'logs': {
            'List Logs': ListLogs,
            'Listen Logs': LogsListener
        }
    }

    def get(self, request):
        links_set = dict(self.unprotected_links)

        if request.user.is_superuser:
            for links_group_key in self.protected_links:
                if links_group_key in links_set:
                    links_set[links_group_key] = dict(links_set[links_group_key])
                else:
                    links_set[links_group_key] = {}
                links_set[links_group_key].update(self.protected_links[links_group_key])

        schema = coreapi.Document(
            title='Example API',
            content=links_set
        )
        return Response(schema)
