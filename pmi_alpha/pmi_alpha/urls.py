"""pmi_alpha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views




urlpatterns = [
    url(r'^admin/', admin.site.urls, name = 'admin'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^clockin/',include('clockin.urls')),
    url(r'^RSR/',include('RSR.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^/CRM', include('common.urls', namespace='common')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^leads/', include('leads.urls', namespace='leads')),
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),
    url(r'^organizations/', include('organizations.urls', namespace='organizations')),
    url(r'^oppurtunities/', include('oppurtunity.urls', namespace='oppurtunities')),
    url(r'^activities/', include('activity.urls', namespace='activities')),
    url(r'^cases/', include('cases.urls', namespace='cases')),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
