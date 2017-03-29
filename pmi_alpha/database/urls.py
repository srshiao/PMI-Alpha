from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.tables, name='tables'),
   url(r'^vendor/(?P<pk>[0-9]+)/$', views.Vendor_DetailView.as_view(), name='vendor_detail'),
   url(r'^employee/(?P<pk>[0-9]+)/$', views.Employee_DetailView.as_view(), name='detail'),
   url(r'^googlegroup/(?P<pk>[0-9]+)/$', views.GoogleGroup_DetailView.as_view(), name='detail'),
   url(r'^customer/(?P<pk>[0-9]+)/$', views.Customer_DetailView.as_view(), name='detail'),
   url(r'^contract/(?P<pk>[0-9]+)/$', views.Contract_DetailView.as_view(), name='detail'),
   url(r'^partner/(?P<pk>[0-9]+)/$', views.Partner_DetailView.as_view(), name='detail'),
   url(r'^department/(?P<pk>[0-9]+)/$', views.Department_DetailView.as_view(), name='detail'),
   url(r'^poc/(?P<pk>[0-9]+)/$', views.POC_DetailView.as_view(), name='detail'),

   url(r'^add_employee/$', views.add_employee, name= 'add employee'),
]
