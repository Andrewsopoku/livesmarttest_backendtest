from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from swagger_schema import SwaggerTestSchemaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bloodtests/', include('bloodtests.urls')),
]
if settings.DEBUG:
    urlpatterns.append(path('api/docs/', SwaggerTestSchemaView.as_view()))
