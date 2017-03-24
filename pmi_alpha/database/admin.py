from django.contrib import admin
from .models import *

admin.site.register(Vendor)
admin.site.register(Employee)
admin.site.register(GoogleGroup)
admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(Partner)
admin.site.register(Department)
admin.site.register(Department_Employee)
admin.site.register(Contract_Employee)
admin.site.register(Customer_Vendor)
admin.site.register(Customer_Employee)
admin.site.register(Customer_Partner)
admin.site.register(POC)
admin.site.register(Vendor_Contract)
admin.site.register(GoogleGroup_Employee)



# Register your models here.
