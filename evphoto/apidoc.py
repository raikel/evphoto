from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="EVPHOTO Api",
        default_version='v1',
        description="Capture an image and display it to a web page",
        contact=openapi.Contact(email="raikelbl@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# noinspection PyUnresolvedReferences
swagger_view = schema_view.with_ui('swagger', cache_timeout=3600)
# noinspection PyUnresolvedReferences
redoc_view = schema_view.with_ui('redoc', cache_timeout=3600)

