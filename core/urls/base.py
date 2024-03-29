"""omega_champions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path,re_path
from .auth import auth_urlpatterns
# from core.views.base import MyFetchView
# from apps.encryption.constants import FETCH_URL_NAME

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # re_path(r"^fetch/(?P<path>.+)", MyFetchView.as_view(), name=FETCH_URL_NAME),

]
urlpatterns += i18n_patterns(path("admin/", admin.site.urls),
                             # path("", include("dashboard.urls")),
                             )
urlpatterns += auth_urlpatterns

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
