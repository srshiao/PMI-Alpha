from django.shortcuts import render
from django_tables2 import RequestConfig
from .forms import *
from .models import *
from .tables import *
from .filters import *
from django.views import generic
from django.http import HttpResponseRedirect
from watson import search as watson
from django.views.generic import ListView
from django.views.generic import TemplateView
from django_tables2 import SingleTableView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class Vendor_DetailView(generic.DetailView):

    model = Vendor
    template_name = 'database/detail.html'

class Employee_DetailView(generic.DetailView):
    model = Employee
    template_name = 'database/detail.html'

class GoogleGroup_DetailView(generic.DetailView):
    model = GoogleGroup
    template_name = 'database/detail.html'

class Customer_DetailView(generic.DetailView):
    model = Customer
    template_name = 'database/detail.html'

class Contract_DetailView(generic.DetailView):
    model = Contract
    template_name = 'database/detail.html'

class Partner_DetailView(generic.DetailView):
    model = Partner
    template_name = 'database/detail.html'

class Department_DetailView(generic.DetailView):
    model = Department
    template_name = 'database/detail.html'

class POC_DetailView(generic.DetailView):
    model = POC
    template_name = 'database/detail.html'

def tables(request):
    vendor_table = VendorTable(Vendor.objects.all())
    employee_table = EmployeeTable(Employee.objects.all())
    googlegroup_table = GoogleGroupTable(GoogleGroup.objects.all())
    customer_table = CustomerTable(Customer.objects.all())
    contract_table = ContractTable(Contract.objects.all())
    partner_table = PartnerTable(Partner.objects.all())
    department_table = DepartmentTable(Department.objects.all())
    department_employee_table = Department_EmployeeTable(Department_Employee.objects.all())
    contract_employee_table = Contract_EmployeeTable(Contract_Employee.objects.all())
    customer_vendor_table = Customer_VendorTable(Customer_Vendor.objects.all())
    customer_employee_table = Customer_EmployeeTable(Customer_Employee.objects.all())
    customer_partner_table = Customer_PartnerTable(Customer_Partner.objects.all())
    poc_table = POCTable(POC.objects.all())
    vendor_contract_table = Vendor_ContractTable(Vendor_Contract.objects.all())
    googlegroup_employee_table = GoogleGroup_EmployeeTable(GoogleGroup_Employee.objects.all())


    RequestConfig(request).configure(vendor_table)
    RequestConfig(request).configure(employee_table)
    RequestConfig(request).configure(googlegroup_table)
    RequestConfig(request).configure(customer_table)
    RequestConfig(request).configure(contract_table)
    RequestConfig(request).configure(partner_table)
    RequestConfig(request).configure(department_table)
    RequestConfig(request).configure(department_employee_table)
    RequestConfig(request).configure(contract_employee_table)
    RequestConfig(request).configure(customer_vendor_table)
    RequestConfig(request).configure(customer_employee_table)
    RequestConfig(request).configure(customer_partner_table)
    RequestConfig(request).configure(poc_table)
    RequestConfig(request).configure(vendor_contract_table)
    RequestConfig(request).configure(googlegroup_employee_table)

    search_results = watson.search("Noah")

    for result in search_results:
        print (result.title, result.url)

    return render(request, 'database/tables.html',
    	{'vendor': vendor_table,
    	'employee':employee_table,
    	'googlegroup':googlegroup_table,
    	'customer': customer_table,
    	'contract':contract_table,
    	'partner':partner_table,
    	'department': department_table,
    	'department_employee':department_employee_table,
    	'contract_employee':contract_employee_table,
    	'customer_vendor': customer_vendor_table,
    	'customer_employee':customer_employee_table,
    	'customer_partner':customer_partner_table,
    	'poc': poc_table,
    	'vendor_contract':vendor_contract_table,
    	'googlegroup_employee':googlegroup_employee_table,
        'search_results':search_results,})


def add_vendor(request):
    form = VendorForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

def add_employee(request):
    form = EmployeeForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

def add_gg(request):
    form = GoogleGroupForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)


def add_customer(request):
    form = CustomerForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

def add_contract(request):
    form = ContractForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

def add_partner(request):
    form = PartnerForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)


def add_department(request):
    form = DepartmentForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

def add_poc(request):
    form = POCForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

def search (request):

    return render(request, 'database/search.html')

def dashboard(request):
    return render(request, 'database/dashboard.html', {})

def add_record(request):
    return render(request, 'database/add_record.html', {})
def basic_search(request):
    return render(request, 'database/basic_search.html', {})
def advanced_search(request):
    return render(request, 'database/advanced_search.html', {})
def select_table(request):
    return render(request, 'database/select_view.html', {})
#CHANGES
class VendorListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.Vendor'
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return Vendor.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VendorListView, self).get_context_data(**kwargs)
        filter = VendorListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = VendorListFormHelper()
        table = VendorTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class EmployeeListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return Employee.objects.all()

    def get_context_data(self, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        filter = EmployeeListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = EmployeeListFormHelper()
        table = EmployeeTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class GGListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return GoogleGroup.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GGListView, self).get_context_data(**kwargs)
        filter = GGListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = GGListFormHelper()
        table = GoogleGroupTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class CustomerListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return Customer.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        filter = CustomerListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = CustomerListFormHelper()
        table = CustomerTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context
class ContractListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return Contract.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ContractListView, self).get_context_data(**kwargs)
        filter = ContractListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = ContractListFormHelper()
        table = ContractTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class PartnerListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return Partner.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        filter = PartnerListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = PartnerListFormHelper()
        table = PartnerTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class DepartmentListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return Department.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        filter = DepartmentListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = DepartmentListFormHelper()
        table = DepartmentTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

class POCListView(TemplateView):
    template_name = 'database/searchable.html'

    def get_queryset(self, **kwargs):
        return POC.objects.all()

    def get_context_data(self, **kwargs):
        context = super(POCListView, self).get_context_data(**kwargs)
        filter = POCListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = POCListFormHelper()
        table = POCTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context
