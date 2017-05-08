#Create Django-Generated forms. Used for adding/editing objects in database. 
#Second section of forms.py used for generating searchable tables. 

#TODO CORRESPOND WITH USERS, CHANGE WHICH FIELDS ARE AVAILABLE TO BE SEARCHED BY
#ACCORDINGLY

from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton


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
    def __init__(self, *args, **kwargs):

        super(DepartmentForm, self).__init__(*args, **kwargs)
        # CHECK: TypedMultipleChoiceField
        self.fields['Employees']=forms.ModelChoiceField(queryset=Employee.objects.all())

class POCForm(forms.ModelForm):
    class Meta:

        model = POC
        fields = '__all__'


#KEY COMPONENT TO SEARCH TABLES. TO ADD/CHANGE SEARCH-BY-FIELDS EDIT THE ITEMS IN THE "FIELDSET"

class VendorListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Vendor Records',       
                    'LegalName',
                    'POC'
                ),
              Submit('submit', 'Apply Filter'),
    )

class EmployeeListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Employee Records',       
                    'FName',
                    'LName',
                    'HUBzone',
                    'VendorID',
                    'DateOfHire',
                    'EmployementStatus',
                    #'date_between',

                ),
                #'resource_first_name',
                #'resource_last_name',
                #'HUBzone',
                #'employment_status',
              Submit('submit', 'Apply Filter'),
    )


class GGListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Google Group Records',       
                    'Name',
                    'Admin'
                ),
              Submit('submit', 'Apply Filter'),
    )

class CustomerListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Customer Records',       
                    'LegalName',
                ),
              Submit('submit', 'Apply Filter'),
    )

class ContractListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Contract Records',       
                    'IssuingCompany',
                    'ContractNumber',

                ),
              Submit('submit', 'Apply Filter'),
    )

class PartnerListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Partner Records',       
                    'LegalName',
                ),
              Submit('submit', 'Apply Filter'),
    )

class DepartmentListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Department Records',       
                    'ContractID',
                    'CustomerID',
                    'Name',
                    'Supervisor'

                ),
              Submit('submit', 'Apply Filter'),
    )

class POCListFormHelper(FormHelper):    
    form_method = 'GET'
    FormHelper.form_class = 'form-horizontal'
    field_class = 'col-lg-6'
    label_class = 'col-lg-3'
    layout = Layout(
         Fieldset(
                    '<i class="fa fa-search"></i> Search Point of Contact Records',       
                    InlineField('FName'),
                    InlineField('LName'),
                    'PartnerID',
                    'ContractID',
                    'CustomerID',

                ),
              Submit('submit', 'Apply Filter'),
    )
