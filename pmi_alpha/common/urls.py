from django.conf.urls import url
from common import views
from django.contrib.auth import views as auth_views

app_name = 'common'


urlpatterns = [
    url(r'^$', views.home, name="home-crm"),
    url(r'^login/$', views.login_crm, name="home-crm"),
    url(r'^registration/$', views.register_page, name='create-crm')
]
