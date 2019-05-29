"""schoolapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import os

from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from schoolapps.settings import BASE_DIR


def manifest(request):
    return serve(request, "manifest.json")


def serviceworker(request):
    return serve(request, "common/pwabuilder-sw.js")


urlpatterns = [
    #############
    # Dashboard #
    #############
    path('', include('dashboard.urls')),

    ########
    # Auth #
    ########
    path('accounts/', include('django.contrib.auth.urls')),

    #######
    # AUB #
    #######
    path('aub/', include('aub.urls')),

    #############
    # TIMETABLE #
    #############
    path('timetable/', include('timetable.urls')),

    ########
    # MENU #
    ########
    path('menu/', include('menu.urls')),

    #########
    # Admin #
    #########
    path("debug/", include("debug.urls")),
    path('settings/', include('dbsettings.urls')),
    path('admin/', admin.site.urls),

    ###########
    # SUPPORT #
    ###########
    path('support/', include('support.urls')),

    #######
    # FAQ #
    #######
    path('faq/', include('faq.urls')),

    path("pwabuilder-sw.js", serviceworker),

    path('martor/', include('martor.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'dashboard.views.error_404'
