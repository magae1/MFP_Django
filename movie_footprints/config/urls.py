"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from knox import views as knox_views

from core.views import LoginView as KnoxLoginView

router = DefaultRouter()

knox_patterns = [
    path('api/login/', KnoxLoginView.as_view(), name="login"),
    path('api/logout/', knox_views.LogoutView.as_view(), name="logout"),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name="logout-all"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + knox_patterns

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
