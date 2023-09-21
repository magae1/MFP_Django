from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from users.views import (
    AccountCreateViewSet,
    ProfileViewSet,
    AccountViewSet,
    LogInView,
    RefreshView,
    LogOutView,
)

router = DefaultRouter()
router.register(r'auth/signup', AccountCreateViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'account', AccountViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', LogInView.as_view(), name="로그인"),
    path('api/auth/refresh/', RefreshView.as_view(), name="토큰 갱신"),
    path('api/auth/logout/', LogOutView.as_view(), name="로그아웃"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += ([
        path("__debug__/", include("debug_toolbar.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
                    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
