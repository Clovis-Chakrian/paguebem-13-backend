from django.contrib import admin # type: ignore
from django.urls import path , include # type: ignore
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Residência - Squad 13",
        default_version='v1',
        description="API dos Índices de Reputação",
        license=openapi.License(name="Awesome License"),
    ),
    # url='https://paguebem-api.chacha.vps-kinghost.net',
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('api/', include('pagamentos.urls')),
    path("admin/", admin.site.urls),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
