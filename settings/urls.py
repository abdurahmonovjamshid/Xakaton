from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser


schema_view = get_schema_view(
    openapi.Info(
        title="DOCUMENTATION",
        description="REST API",
        default_version="1.0.0",
        terms_of_service="ScienTech Solution",
        contact=openapi.Contact(email="admin@gmail.com"),
        license=openapi.License(name="Private"),
    ),
    public=False,
    permission_classes=(IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include([
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
        path('accounts/', include('users.urls')),
        path('store/', include('store.urls')),
        path('common/', include('core.urls')),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

        
    ])),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
