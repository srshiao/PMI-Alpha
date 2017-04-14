from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.forms import ModelForm


# USE THIS TO ENABLE SCROLL DOWN SELECTION
GENDERCHOICE = (
	('M', 'Male'),
	('F', 'Female'),
	('O', 'Other'),
	)
CTYPE = (
	('LH', 'Labor Hour'),
	('T', 'TNM'),
	('F','FFP'),

	)
class Vendor(models.Model):

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('vendor_detail', args=[str(self.id)])

	def __str__(self):
		# Class Name: name
   		# return self.__class__.__name__ + ": " + self.LegalName
   		return self.LegalName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			if field.name == "employee":
				field.verbose_name = "Employees"
				# employee_set = Employee.objects.filter(VendorID = self.id)
				#iterates over given query set and returns string representations.
				values = ""
				for employee in self.employee_set.all():
					values = values + " \n " + "\xa0\xa0\xa0\xa0" + employee.__str__()
				yield(field,values)
			else:
				value = getattr(self, field.name, None)
				yield (field, value)

	LegalName = models.CharField(_("Legal Name"), max_length = 50, default = None)
	ZipCode = models.CharField(_("Zip Code"), max_length = 10, default = None)
	TIN = models.IntegerField(default = None)
	State = models.CharField(max_length = 10, default = None)
	POC = models.CharField(_("Point of Contact"), max_length = 50, default = None)
	Phone = models.CharField(_("phone"), max_length = 20, default = None)
	Fax = models.CharField(_("Fax"), max_length = 50, default = None)
	Email = models.CharField(_("Email"), max_length = 50, default = None)
	DUNs = models.CharField(_("DUNs"), max_length = 50, default = None)
	DBA = models.CharField(_("DBA"), max_length = 50, default = None)
	Country = models.CharField(_("Country"), max_length = 20, default = None)
	City = models.CharField(_("City"), max_length = 20, default = None)
	CAGE = models.CharField(_("CAGE"), max_length = 50, default = None)
	Address = models.CharField(_("Address"), max_length = 50, default = None)


class Employee(models.Model):
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('employee_detail', args=[str(self.id)])

	def __str__(self):
   		return self.FName + " " + self.LName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	SubmittedViaWebform = models.BooleanField(_("Submitted Via Webform (T/F)"), default = True)
	FName = models.CharField(_("Resource First Name"), max_length = 20, default = None)
	MName = models.CharField(_("Resource Middle Name"), max_length = 20, default = None)
	LName = models.CharField(_("Resource Last Name"), max_length = 20, default = None)

	VendorID = models.ForeignKey(Vendor)


	CreatedBy = models.CharField(_("Created By"), max_length = 20, default = None)
	Created = models.DateField(_("Created"), default=datetime.date.today)
	RequestType = models.CharField(_("Request Type"), max_length = 20, default = None)
	ClockSequence = models.CharField(_("Clock Sequence"), max_length = 20, default = None)
	EffectiveDate = models.DateField(_("Effective Date of Change in Record"), default=datetime.date.today)
	PayrollCompany = models.CharField(_("Payroll Company"), max_length = 20, default = None)
	ProbationAlert = models.DateField(_("Probation Alert"), default=datetime.date.today)
	ProjectFunctionalTitle = models.CharField(_("Project Functional Title"), max_length = 50, default = None)
	GbSecruityAccessRequest = models.CharField(_("Gb Security Access Request"), max_length = 50, default = None)
	OfferContractSent = models.BooleanField(_("Offer Contract Sent"), default = True)
	OfferContractNDAFE = models.DateField(_("Offer Contract NDA FE"), default=datetime.date.today)
	CommissionLogged = models.BooleanField(_("Commision Logged"), default = True)
	CommissionDueDate = models.DateField(_("Commission Due Date"), default=datetime.date.today)
	ToolKit = models.BooleanField(_("Tool Kit"), default = True)
	SoftwareRequest = models.CharField(_("Software Request"), max_length = 50, default = None)
	ClockSequenceHistoric = models.CharField(_("ClockSequenceHistoric"), max_length = 50, default = None)

	Gender = models.CharField(_("Gender"), max_length = 10, choices=GENDERCHOICE, default = None)
	PersonalEmail = models.CharField(_("Personal Email"), max_length = 50, default = None)
	PMIEmail = models.CharField(_("PMI Email"), max_length = 50, default = None)
	TypeOfContract = models.CharField(_("Type of Contract"), max_length = 20, default = None)
	Addresses = models.CharField(_("Addresses"), max_length = 30, default = None)
	City = models.CharField(_("City"), max_length = 20, default = None)
	ZipCode = models.CharField(_("Zip code"), max_length = 10, default = None)
	State = models.CharField(_("State"), max_length = 10, default = None)
	Country = models.CharField(_("Country"), max_length = 20, default = None)
	Phone = models.CharField(_("Phone"), max_length = 20, default = None)
	BirthDate = models.DateField(_("Birth Date"), default=datetime.date.today)
	DateOfHire = models.DateField(_("Date of Hire"), default=datetime.date.today)
	PMICareerTitle = models.CharField(_("PMI Career Title    "), max_length = 50, default = None)
	ResourceType= models.CharField(_("Resource Type"), max_length = 20, default = None)
	GSALaborCategory = models.CharField(_("GSA Labor Category"), max_length=20, default = None)
	VacationHour = models.CharField(_("Vacation Hour"), max_length = 20, default = None)
	SickLeaveHour = models.CharField(_("Sick Leave Hour"), max_length = 20, default = None)
	EmployementStatus = models.CharField(_("Employment Status"), max_length = 50, default = None)
	ContractLaborCategory = models.CharField(_("Contract Labor Category"), max_length = 20, default = None)
	RecruitmentSource = models.CharField(_("Recruitment Source"), max_length = 50, default = None)
	ResponsibleRecruiter = models.CharField(_("Responsible Recruiter"), max_length = 50, default = None)
	HUBzone = models.BooleanField(_("HUBzone"), default = True)
	ProbationaryEnd= models.DateField(_("Probationary End"), default=datetime.date.today)
	TerminationDate = models.DateField(_("Termination Date"), default=datetime.date.today)
	Department = models.CharField(_("Department"), max_length = 50, default = None)
	WorkLocation = models.CharField(_("Work Location"), max_length = 50, default = None)
	Billable = models.BooleanField(_("Billable"), default = True)
	SalaryType = models.CharField(_("Salary Type"), max_length = 20, default = None)
	Salary = models.IntegerField(_("Salary"), default = None)
	ClearanceStatus = models.CharField(_("Clearance Status"), max_length = 20, default = None)
	ClearedDate = models.DateField(_("Cleared Date"), default=datetime.date.today)
	ClearedType = models.CharField(_("Cleared Type"), max_length = 20, default = None)
	Rehire = models.BooleanField(_("Rehire (T/F)"), default = True)
	_401KEligible = models.BooleanField(_("401K Eligible"), default = True)
	OrientationDate = models.DateField(_("Orientation Date"), default=datetime.date.today)
	ClientBillRate = models.CharField(_("Client Bill Rate"), max_length = 20, default = None)
	GSA_vehicle = models.CharField(_("GSA Vehicle"), max_length = 50, default = None)
	GSA_rate = models.CharField(_("GSA Rate"), max_length = 50, default = None)
	CAMPINSent = models.CharField(_("CAMPINSent"), max_length = 50, default = None)
	PaycomLogin = models.CharField(_("Paycom Login"), max_length = 50, default = None)
	eFAACT = models.CharField(_("eFAACT"), max_length=50, default = None)
	Computer = models.CharField(_("Computer"), max_length=50, default = None)
	BusinessCard = models.CharField(_("Business Card"), max_length=50, default = None)
	Comments = models.CharField(_("Comments"), max_length = 1000, default = None)


class GoogleGroup(models.Model):
	def __str__(self):
		return self.Name

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	Employees = models.ManyToManyField(Employee, through='GoogleGroup_Employee')

	Name = models.CharField(_("Name"), max_length = 50, default = None)
	Admin = models.CharField(_("Admin"), max_length = 50, default = None)

class Partner(models.Model):
	def __str__(self):
		return self.LegalName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)
	LegalName = models.CharField(_("Legal Name"), max_length = 50, default = None)

	Address = models.CharField(_("Address"), max_length = 50, default = None)
	CAGE = models.CharField(_("CAGE"), max_length = 50, default = None)
	City = models.CharField(_("City"), max_length = 20, default = None)
	ZipCode = models.CharField(_("Zip code"), max_length = 10, default = None)
	State = models.CharField(_("State"), max_length = 10, default = None)
	Country = models.CharField(_("Country"), max_length = 20, default = None)
	Phone = models.CharField(_("Phone"), max_length = 20, default = None)
	Fax = models.CharField(_("Fax"), max_length = 50, default = None)
	Email = models.CharField(_("Email"), max_length = 50, default = None)
	DBA = models.CharField(_("DBA"), max_length = 50, default = None)
	DUNs = models.CharField(_("DUNs"), max_length = 9, default = None)
	POC = models.CharField(_("Point of Contact"), max_length = 50, default = None)
	TIN = models.CharField(_("TIN"), max_length=11, default = None)
	Type = models.CharField(_("Type"), max_length=20, default = None)


class Customer(models.Model):
	def __str__(self):
   		return self.LegalName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	LegalName = models.CharField(_("Legal Name"), max_length = 50, default = None)

	Vendors = models.ManyToManyField(Vendor, through='Customer_Vendor')
	Employees = models.ManyToManyField(Employee, through='Customer_Employee')
	Partners = models.ManyToManyField(Partner, through='Customer_Partner')

	DBA = models.CharField(_("DBA"), max_length = 50, default = None)
	Address = models.CharField(_("Address"), max_length = 50,  default = None)
	City = models.CharField(_("City"), max_length = 20, default = None)
	ZipCode = models.CharField(_("Zip code"), max_length = 10, default = None)
	State = models.CharField(_("State"), max_length = 10, default = None)
	Country = models.CharField(_("Country"), max_length = 20, default = None)
	Phone = models.CharField(_("Phone"), max_length = 20, default = None)
	Fax = models.CharField(_("Fax"), max_length = 50, default = None)
	Email = models.CharField(_("Email"), max_length = 50, default = None)
	DUNs = models.CharField(_("DUNs"), max_length = 9, default = None)
	CAGE = models.CharField(_("CAGE"), max_length = 50, default = None)
	POC = models.CharField(_("Point of Contact"), max_length = 50, default = None)
	TIN = models.CharField(_("TIN"), max_length=11, default = None)

class Contract(models.Model):
	def __str__(self):
   		return self.ContractNumber

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)
	IssuingCompany = models.CharField(_("Issuing Company"), max_length = 50, default = None)
	ContractNumber = models.CharField(_("Contract Number"), max_length = 50, default = None)

	#ContractName = models.CharField(_("Contract Name"), max_length = 50, default = None)
	#ContractType = models.CharField(_("Contract Type"), max_length = 50, default = None, choices = CTYPE)
	DocumentLocation = models.CharField(_("Document Location"), max_length = 50, default = None)
	OrganizationType = models.CharField(_("Organization Type"), max_length = 50, default = None)

	CustomerID = models.ForeignKey(Customer)
	Employees = models.ManyToManyField(Employee, through='Contract_Employee')
	Vendors = models.ManyToManyField(Vendor, through='Vendor_Contract')

	POC = models.CharField(_("Point of Contact"), max_length = 50, default = None)
	EffectiveDate = models.DateField(_("Effective Date"), default=datetime.date.today)
	EndDate = models.DateField(_("End Date"), default=datetime.date.today)
	StartDate = models.DateField(_("Start Date"), default=datetime.date.today)
	Status = models.CharField(_("Status"), max_length = 50, default = None)

	#Clearance = models.CharField(_("Clearance"), max_length = 50, default = None)
	#Scope = models.CharField(_("Scope"), max_length = 50, default = None)
	#ContractValue = models.CharField(_("Contract Value"), max_length = 50, default = None)
	#PlaceOfPerformance = models.CharField(_("Place Of Performance"), max_length = 100, default = None)


	#http://stackoverflow.com/questions/5090047/django-create-a-model-that-lets-you-insert-multiple-values-for-the-same-field

	Comments = models.CharField(_("Comments"), max_length = 1000, default = None)


class Department(models.Model):
	def __str__(self):
   		return self.Name

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	ContractID = models.ForeignKey(Contract)
	CustomerID = models.ForeignKey(Customer)
	Employees = models.ManyToManyField(Employee, through='Department_Employee')

	Name = models.CharField(_("Name"), max_length = 50, default = None)
	Location = models.CharField(_("Location"), max_length = 50, default = None)
	Fax = models.CharField(_("Fax"), max_length = 50, default = None)
	Supervisor = models.CharField(_("Supervisor"), max_length = 50, default = None)
	Phone = models.CharField(_("Phone"), max_length = 50, default = None)

class POC(models.Model):
	def __str__(self):
   		return self.FName + " " + self.LName

	def __iter__(self):
		for field in self._meta.get_fields(include_parents=True, include_hidden=False):
			value = getattr(self, field.name, None)
			yield (field, value)

	FName = models.CharField(_("Resource First Name"), max_length = 20)
	LName = models.CharField(_("Resource Last Name"), max_length = 20)

	PartnerID = models.ForeignKey(Partner)
	ContractID = models.ForeignKey(Contract)
	CustomerID = models.ForeignKey(Customer)

	Address = models.CharField(_("Address"), max_length = 50)
	Phone = models.CharField(_("Phone"), max_length = 20)
	Email = models.CharField(_("Email"), max_length = 50)


# INTERMEDIARY TABLES

class Department_Employee(models.Model):
	DepartmentID = models.ForeignKey(Department)
	EmployeeID = models.ForeignKey(Employee)
class Contract_Employee(models.Model):
	ContractID = models.ForeignKey(Contract)
	EmployeeID = models.ForeignKey(Employee)

class Customer_Vendor(models.Model):
	CustomerID = models.ForeignKey(Customer)
	VendorID = models.ForeignKey(Vendor)

class Customer_Employee(models.Model):
	CustomerID = models.ForeignKey(Customer)
	EmployeeID = models.ForeignKey(Employee)

class Customer_Partner(models.Model):
	CustomerID = models.ForeignKey(Customer)
	PartnerID = models.ForeignKey(Partner)


class Vendor_Contract(models.Model):
	VendorID = models.ForeignKey(Vendor)
	ContractID = models.ForeignKey(Contract)

class GoogleGroup_Employee(models.Model):
	GoogleGroupID = models.ForeignKey(GoogleGroup)
	EmployeeID = models.ForeignKey(Employee)
