from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

ROOT_URl = "/api/bloodtests/"


class SwaggerTestSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]
    config = {
        "title": "Blood Test Internal API",
        "description": "API documentation for creating and retrieving Blood Test",
        "url": ROOT_URl,
        "patterns": [
            path('', include('bloodtests.urls')),
        ]
    }

    def get(self, request):
        generator = SchemaGenerator(**self.config)
        schema = generator.get_schema(request=request, public=True)
        return Response(schema)
