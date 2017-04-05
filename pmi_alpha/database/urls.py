from django.conf.urls import url
from . import views
from django.conf.urls import include


urlpatterns = [
   url(r'^$', views.tables, name='tables'),
   url(r'^vendor/(?P<pk>[0-9]+)/$', views.Vendor_DetailView.as_view(), name='vendor_detail'),
   url(r'^employee/(?P<pk>[0-9]+)/$', views.Employee_DetailView.as_view(), name='employee_detail'),
   url(r'^googlegroup/(?P<pk>[0-9]+)/$', views.GoogleGroup_DetailView.as_view(), name='detail'),
   url(r'^customer/(?P<pk>[0-9]+)/$', views.Customer_DetailView.as_view(), name='detail'),
   url(r'^contract/(?P<pk>[0-9]+)/$', views.Contract_DetailView.as_view(), name='detail'),
   url(r'^partner/(?P<pk>[0-9]+)/$', views.Partner_DetailView.as_view(), name='detail'),
   url(r'^department/(?P<pk>[0-9]+)/$', views.Department_DetailView.as_view(), name='detail'),
   url(r'^poc/(?P<pk>[0-9]+)/$', views.POC_DetailView.as_view(), name='detail'),

   url(r'^add_vendor/$', views.add_vendor, name= 'add vendor'),
   url(r'^add_employee/$', views.add_employee, name= 'add employee'),
   url(r'^add_gg/$', views.add_gg, name= 'add googlegroup'),
   url(r'^add_customer/$', views.add_customer, name= 'add customer'),
   url(r'^add_contract/$', views.add_contract, name= 'add contract'),
   url(r'^add_partner/$', views.add_partner, name= 'add partner'),
   url(r'^add_department/$', views.add_department, name= 'add department'),
   url(r'^add_poc/$', views.add_poc, name= 'add poc'),

   url(r'^search/', include("watson.urls", namespace="watson")),


   url(r'^dashboard/$', views.dashboard, name= 'dashboard'),




]
