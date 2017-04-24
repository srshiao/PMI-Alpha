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

#Detail Views -> Shows detailed Object Info from table.
class Vendor_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.Vendor'
    model = Vendor
    template_name = 'database/detail.html'

class Employee_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.Employee'
    model = Employee
    template_name = 'database/detail.html'

class GoogleGroup_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.GoogleGroup'
    model = GoogleGroup
    template_name = 'database/detail.html'

class Customer_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.Customer'
    model = Customer
    template_name = 'database/detail.html'

class Contract_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.Contract'
    model = Contract
    template_name = 'database/detail.html'

class Partner_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.Partner'
    model = Partner
    template_name = 'database/detail.html'

class Department_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.Department'
    model = Department
    template_name = 'database/detail.html'

class POC_DetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'database.POC'
    model = POC
    template_name = 'database/detail.html'

#Shows All Tables in One Page
@login_required
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

    # search_results = watson.search("Noah",  exclude=(Employee,))

    # for result in search_results:
    #     print (result.title, result.url)

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
        })


#add_* --> renders add page to add new objects to database
@login_required
def add_vendor(request):
    form = VendorForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

@login_required
def add_employee(request):
    form = EmployeeForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')

    return render(request, 'database/add_new.html', context)

@login_required
def add_gg(request):
    form = GoogleGroupForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

@login_required
def add_customer(request):
    permission_required = 'database.Customer'
    form = CustomerForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

@login_required
def add_contract(request):
    form = ContractForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

@login_required
def add_partner(request):
    form = PartnerForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)


@login_required
def add_department(request):
    form = DepartmentForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)

@login_required
def add_poc(request):
    form = POCForm(request.POST or None);
    context = {
        'form' : form
    }
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/database/')


    return render(request, 'database/add_new.html', context)


#HTML PAGES USED FOR REDIRECTION
@login_required
def search (request):
    return render(request, 'database/search.html')
@login_required
def dashboard(request):
    return render(request, 'database/dashboard.html', {})
@login_required
def add_record(request):
    return render(request, 'database/add_record.html', {})
@login_required
def basic_search(request):
    return render(request, 'database/basic_search.html', {})
@login_required
def advanced_search(request):
    return render(request, 'database/advanced_search.html', {})
@login_required
def select_table(request):
    return render(request, 'database/select_view.html', {})

#ADVANCED TABLES, SEARCH/FILTER
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

class EmployeeListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.Employee'
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

class GGListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.GoogleGroup'
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

class CustomerListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.Customer'
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
class ContractListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.Contract'
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

class PartnerListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.Partner'
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

class DepartmentListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.Department'
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

class POCListView(PermissionRequiredMixin,TemplateView):
    permission_required = 'database.POC'
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
