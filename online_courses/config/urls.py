from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Posts API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger'), name='swagger'),
    path('webhook/', include('apps.zoom.urls'))
]
