from django import forms
from .models import *
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
#from crispy_forms.bootstrap import InlineField, FormActions, StrictButton

class VendorForm(forms.ModelForm):
    class Meta:

        model = Vendor
        fields = '__all__'

class EmployeeForm(forms.ModelForm):
    class Meta:

        model = Employee
        fields = '__all__'

class GoogleGroupForm(forms.ModelForm):
    class Meta:

        model = GoogleGroup
        fields = '__all__'


class PartnerForm(forms.ModelForm):
    class Meta:

        model = Partner
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:

        model = Customer
        fields = '__all__'

class ContractForm(forms.ModelForm):
    class Meta:

        model = Contract
        fields = '__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:

        model = Department
        fields = '__all__'

class POCForm(forms.ModelForm):
    class Meta:

        model = POC
        fields = '__all__'
