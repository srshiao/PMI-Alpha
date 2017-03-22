from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import *
from .tables import *

def tables(request):
    vendors_table = VendorsTable(Vendors.objects.all())
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


    RequestConfig(request).configure(vendors_table)
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


    return render(request, 'database/tables.html', 
    	{'vendors': vendors_table, 
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
    	'googlegroup_employee':googlegroup_employee_table, })

