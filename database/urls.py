from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.tables, name='tables'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
