import django_filters
from .models import *
from django import forms
from django.forms import TextInput
from dal import autocomplete

class UploadListFilter(django_filters.FilterSet):

  TYPERESUME_CHOICES = (('Employee', 'Employee'),
  ('Intern', 'Intern'),
  ('Prospective Employee', 'Prospective Employee'),
  ('Prospective Intern', 'Prospective Intern'),

)

  type = django_filters.ChoiceFilter(choices=TYPERESUME_CHOICES)
  class Meta:
      model = Document
      fields = ['type']
      order_by = ['pk']



class PersonFilter(django_filters.FilterSet):

    WORKAUTHORIZATION_CHOICES = (
        ('Citizenship', 'Citizenship'),
        ('Permanent Resident', 'Permanent Resident'),
        ('Visa', 'Visa')
    )

    TYPERESUME_CHOICES = (('Employee', 'Employee'),
    ('Intern', 'Intern'),
    ('Prospective Employee', 'Prospective Employee'),
    ('Prospective Intern', 'Prospective Intern'))

    Levels = (
    ('0','0'),
    ('1', '1'),
    ('2', '1'),
    ('3', '3'),
    ('4', '4'),
    ('5','5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10','10')
)
    TypeResume = django_filters.ChoiceFilter(name='TypeResume', choices=TYPERESUME_CHOICES)

    UploadDate = django_filters.DateFilter(name='CreationDate',input_formats=['%Y-%m-%d', '%m-%d-%Y', '%Y/%m/%d','%m/%d/%Y', '%Y%m%d', '%m%d%Y']\
    , lookup_expr='icontains')

    SchoolAttend = django_filters.ModelChoiceFilter(name='persontoschool__SchoolID', queryset=School.objects.all().order_by('Name'),
                                                    to_field_name='Name')
    GraduateDate = django_filters.ModelChoiceFilter(name='persontoschool__GradDate',
                                                    queryset=PersonToSchool.objects.values_list('GradDate',flat=True).
                                                    distinct().order_by('GradDate'),
                                                    to_field_name='GradDate')
    Major = django_filters.ModelChoiceFilter(name='persontoschool__MajorID', queryset=Major.objects.all().order_by('Name').distinct())
    DegreeLevel = django_filters.ModelChoiceFilter(name='persontoschool__SchoolID__DegreeLevel',
                                                   queryset=School.objects.values_list('DegreeLevel',flat=True).distinct(),
                                                   to_field_name='DegreeLevel')
    GPAlb = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='gte')
    GPAub = django_filters.NumberFilter(name='persontoschool__GPA',lookup_expr='lt')
    Coursework = django_filters.ModelMultipleChoiceFilter(name='persontocourse__Desc',
                                                  queryset=PersonToCourse.objects.distinct().order_by('Desc'),
                                                  widget=autocomplete.ModelSelect2Multiple(
                                                  url='RSR:Coursework-autocomplete'))
    Language = django_filters.ModelMultipleChoiceFilter(name='persontolanguage__LangID',
                                                queryset=LanguageSpoken.objects.all(),
                                                widget=autocomplete.ModelSelect2Multiple(url='RSR:LanguageSpoken-autocomplete'))
    Skills = django_filters.ModelMultipleChoiceFilter(name='persontoskills__SkillsID',
                                              queryset=Skills.objects.all().order_by('Name').distinct(),
                                              widget=autocomplete.ModelSelect2Multiple(url='RSR:Skills-autocomplete'))
    Skills_AND = django_filters.ModelMultipleChoiceFilter(name='persontoskills__SkillsID',
                                                      queryset=Skills.queryset.order_by('Name').distinct(),
                                                      widget=autocomplete.ModelSelect2Multiple(
                                                          url='RSR:Skills-autocomplete'),
                                                          conjoined = True)
    YearOfExperienceForSkill = django_filters.ModelChoiceFilter(name='persontoskills__YearsOfExperience',lookup_expr='gte',
                                                                queryset=PersonToSkills.objects.values_list('YearsOfExperience',flat=True).
                                                                order_by('YearsOfExperience').distinct(),to_field_name='YearsOfExperience')
    ProfessionalDevelopment = django_filters.ModelMultipleChoiceFilter(name='persontoprofessionaldevelopment__ProfID',
                                                               queryset=ProfessionalDevelopment.objects.all().order_by('Name'),
                                                               widget=autocomplete.ModelSelect2Multiple(url='RSR:ProfessionalDevelopment-autocomplete'))
    Award = django_filters.ModelMultipleChoiceFilter(name='persontoawards__AwardID',
                                             queryset=Awards.objects.all().order_by('Name').distinct(),
                                             widget=autocomplete.ModelSelect2Multiple(url='RSR:Awards-autocomplete'))
    CompanyWorked = django_filters.ModelMultipleChoiceFilter(name='persontocompany__CompanyID',
                                                     queryset=Company.objects.all().order_by('Name').distinct(),
                                                     widget=autocomplete.ModelSelect2Multiple(url='RSR:Company-autocomplete'))
    Title = django_filters.ModelMultipleChoiceFilter(name='persontocompany__Title',
                                             queryset=PersonToCompany.objects.order_by('Title').distinct(),
                                             widget=autocomplete.ModelSelect2Multiple(
                                                 url='RSR:Title-autocomplete'))
    Volunteering = django_filters.ModelMultipleChoiceFilter(name='persontovolunteering__VolunID',
                                                    queryset=Volunteering.objects.all().distinct().order_by('Name'),
                                                    widget=autocomplete.ModelSelect2Multiple(url='RSR:Volunteering-autocomplete'))
    Club_Hobby = django_filters.ModelChoiceFilter(name='persontoclubshobbies_set__CHID',
                                                  queryset=Clubs_Hobbies.objects.all().distinct().order_by('Name'),
                                                  to_field_name='Name')
    SecurityClearance = django_filters.ModelChoiceFilter(name='persontoclearance__ClearanceLevel',
                                                         queryset=Clearance.objects.all().distinct())
    WorkAuthorization = django_filters.ChoiceFilter(name='WorkAuthorization', choices=WORKAUTHORIZATION_CHOICES)
    Name = django_filters.ModelMultipleChoiceFilter(name='Name', queryset=Person.objects.all(),
                                          widget=autocomplete.ModelSelect2Multiple(url='RSR:Name-autocomplete'))
    Level = django_filters.ModelChoiceFilter(name='persontoskills__Level',queryset=PersonToSkills.objects.values_list('Level',flat=True).
    order_by('Level').distinct(),to_field_name='Level')

    class Meta:
        model = Person
        fields = ['SchoolAttend', 'GraduateDate', 'Major', 'DegreeLevel', 'GPAlb', 'GPAub','Language', 'Skills',
                   'YearOfExperienceForSkill', 'ProfessionalDevelopment', 'Award', 'CompanyWorked', 'Title',
                   'SecurityClearance', 'Volunteering', 'Club_Hobby','TypeResume','UploadDate','Name', 'Skills_AND','Level']
