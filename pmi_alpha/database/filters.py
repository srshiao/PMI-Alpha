import django_filters
from .models import *


class VendorListFilter(django_filters.FilterSet):

  class Meta:
    model = Vendor
    fields =  '__all__'
    order_by = ['pk']

class EmployeeListFilter(django_filters.FilterSet):

  class Meta:
    model = Employee
    fields =  '__all__'
    order_by = ['pk']
class GGListFilter(django_filters.FilterSet):

  class Meta:
    model = GoogleGroup
    fields =  '__all__'
    order_by = ['pk']

class CustomerListFilter(django_filters.FilterSet):

  class Meta:
    model = Customer
    fields =  '__all__'
    order_by = ['pk']
class ContractListFilter(django_filters.FilterSet):

  class Meta:
    model = Contract
    fields =  '__all__'
    order_by = ['pk']

class PartnersListFilter(django_filters.FilterSet):

  class Meta:
    model = Partner
    fields =  '__all__'
    order_by = ['pk']

class DepartmentListFilter(django_filters.FilterSet):

  class Meta:
    model = Department
    fields =  '__all__'
    order_by = ['pk']

class POCListFilter(django_filters.FilterSet):

  class Meta:
    model = POC
    fields =  '__all__'
    order_by = ['pk']