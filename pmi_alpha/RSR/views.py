# -*- coding: utf-8 -*-
from .models import *
import docx2txt
from django.utils import timezone
from itertools import chain
from gensim.models import Word2Vec
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

import os

# Create your views here.
#=======
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

from RSR.models import *
from RSR.forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .filters import *
###Search #
from django.db.models import Q
from RSR.persondetails import Detail
from RSR.persondetails2 import Detail2
from django.views.generic.edit import UpdateView
from dal import autocomplete
from background_task import background
from datetime import datetime
### json Parsing ##
import json
from .parsing import *
###TESTING OCR

from PIL import Image
from wand.image import Image as IMG
import pytesseract
import textract

### Limit group###

from django.contrib.auth.decorators import user_passes_test



@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    return render(request,'dashboard/barchart.html')


@login_required
def main(request):
    return render(request, 'main.html')


def get_string(name):
    img=Image.open(name)
    utf8_text = pytesseract.image_to_string(img)
    utf8_text = str(utf8_text.encode('ascii', 'ignore'))
    return utf8_text


def punct_space(token):
    "helper that elimates puncations and whitespace"
    return token.is_punct or token.is_space

def line_review(filename):
    "read resumes from the file and un-escapes orignal line break"
    with codecs.open(filename,encoding='utf_8') as f:
        for res in f:
            yield res.replace('\\n','\n')

def lemmatized_sentence_corpus(filename):
    "use spacy to parse, lemmatize and yield sentences"
    for parsed_res in nlp.pipe(line_review(filename),batch_size=10000,n_threads=3):
        for sent in parsed_res.sents:
            yield u' '.join([token.lemma_ for token in sent if not punct_space(token)])

@background(schedule=timezone.now())
def load_parsing_files():
    normal_res  = ''
    docs = Document.objects.all()
    print(docs)
    for doc in docs:
        normal_res = normal_res + doc.wordstr
    res2vec = Word2Vec(normal_res,size=300,window=10,sg=1,workers=4,min_count=5)
    res2vec.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','vector_models1')))

    for i in range(1,15):
         res2vec.train(normal_res,total_examples=res2vec.corpus_count, epochs=res2vec.iter)
         res2vec.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..','www','Parsing','vector_models1')))

@background(schedule=timezone.now())
def parse_back(words,doc,doc_type):
    print('After',words,doc,doc_type)
    parsed_json  = parse_file(words)
    #either load json, or recieve json file
    js = parsed_json

    #iterate through json file
    print('\n\n',js,'\n\n')
    #initialize person out side of for loop/if statements so we can use it later
    person = Person(Name="temp")
    for key in js['person']:
        if key == "name":
            person.Name = js['person'][key]
        elif key == "email":
            if js['person'][key] == None:
                person.Email = "Not parsed"
            else:
                person.Email = js['person'][key]
        elif key == "address":
            if js['person'][key] == None:
                person.Address = "Not parsed"
            else:
                person.Address = js['person'][key]
        elif key == "zipcode":
            if js['person'][key] == None:
                person.ZipCode = "Not parsed"
            else:
                person.ZipCode = js['person'][key]
        elif key == "state":
            if js['person'][key] == None:
                person.State = 'Not Parsed'
            else:
                person.State = js['person'][key]
        elif key == "phone":
            person.PhoneNumber = js['person'][key]
        elif key == "linkedin":
            person.Linkedin = js['person'][key]
        elif key == "github":
            person.GitHub = js['person'][key]
    person.Resume = doc
    person.TypeResume = doc_type
    person.save()
    for label in js:
        if label == "skills":
            for key in js[label]:
                #check to see if skill exists
                query_set=Skills.objects.all()
                query_set=query_set.filter(Name=key["skill"])
                #if skill does not exist create skill
                if not query_set:
                    query_set = Skills(Name = key["skill"])
                    query_set.save()
                #if skill does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                #person.save(commit = False)
                skill_to_person = PersonToSkills(SkillsID = query_set, PersonID = person,YearsOfExperience = key["YearsOfExperience"])
                skill_to_person.save()

        elif label == "work":
            for key in js[label]:
                #check to see if company exists
                query_set=Company.objects.all()

                query_set=query_set.filter(Name=key["company"])
                #if company does not exist create skill
                if not query_set:
                    query_set = Company(Name = key["company"])
                    query_set.save()
                #if company does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                #intermediary table stuff
                company_to_person = PersonToCompany(CompanyID = query_set, PersonID = person,
                    Title = key["title"],
                    ExperienceOnJob = key["experience"],
                    # StartDate = key["startDate"],
                    # EndDate = key["endDate"],
                    Desc = key["summary"])
                company_to_person.save()

        elif label == "education":
            for key in js[label]:
                #check to see if School exists
                query_set=School.objects.all()
                query_set=query_set.filter(Name=key["school"]["name"]).filter(DegreeLevel = key["school"]["degreeLevel"])
                #if School does not exist create skill
                if not query_set:
                    query_set = School(Name = key["school"]["name"], DegreeLevel = key["school"]["degreeLevel"])
                    query_set.save()
                #if School does exist, grab first match from queryset
                else:
                    query_set = query_set[0]

                # NOW DO MAJOR
                query_set_1=Major.objects.all()
                query_set_1=query_set_1.filter(Name=key["major"]["major"]).filter(Dept__icontains = key["major"]["dept"]).filter(MajorMinor__icontains = key["major"]["major/minor"])
                if not query_set_1:
                    query_set_1 = Major(Name = key["major"]["major"], Dept = key["major"]["dept"], MajorMinor = key["major"]["major/minor"])
                    query_set_1.save()
                #if School does exist, grab first match from queryset
                else:
                    query_set_1 = query_set_1[0]

                #intermediary table stuff
                #person.save(commit = False)
                ed_to_person = PersonToSchool(SchoolID = query_set, PersonID = person, MajorID = query_set_1,
                    GPA = key["GPA"],
                    GradDate = key["gradDate"])
                ed_to_person.save()


        elif label == "sideprojects":
            for key in js[label]:
                #check to see if project exists
                query_set=SideProject.objects.all()
                query_set=query_set.filter(Name=key["name"])
                #if project does not exist create project
                if not query_set:
                    query_set = SideProject(Name = key["name"])
                    query_set.save()
                #if project does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                #intermediary table stuff
                person.save(commit = False)
                project_to_person = PersonToSide(SideID = query_set, PersonID = person, Desc = key["description"])
                project_to_person.save()

        elif label == "award":
            for key in js[label]:
                #check to see if Award exists
                query_set=Awards.objects.all()
                query_set=query_set.filter(Name=key["name"])
                #if Award does not exist create Award
                if not query_set:
                    query_set = Awards(Name = key["name"])
                    query_set.save()
                #if Award does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                #intermediary table stuff
                person.save(commit = False)
                awards_to_person = PersonToAwards(AwardID = query_set, PersonID = person, Desc = key["description"])
                awards_to_person.save()

        elif label == "clearance":
            query_set = Clearance.objects.all()
            query_set = query_set.filter(ClearanceLevel = js[label]["level"])
            if not query_set:
                query_set = Clearance(ClearanceLevel=js[label]["level"])
                query_set.save()
            else:
                query_set = query_set[0]
            cl_to_person = PersonToClearance(PersonID=person, ClearanceLevel = query_set)
            cl_to_person.save()

        elif label == "languages":
            for key in js[label]:
                # check to see if language exists
                query_set = LanguageSpoken.objects.all()
                query_set = query_set.filter(Language=key["language"])
                # if language does not exist create language
                if not query_set:
                    query_set = LanguageSpoken(Language=key["language"])
                    query_set.save()
                # if language does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                # intermediary table stuff
                person.save(commit = False)
                language_to_person = PersonToLanguage(LangID=query_set, PersonID=person)
                language_to_person.save()

        elif label == "clubs":
            for key in js[label]:
                # check to see if club exists
                query_set = Clubs_Hobbies.objects.all()
                query_set = query_set.filter(Name=key["name"])
                # if club does not exist create club
                if not query_set:
                    query_set = Clubs_Hobbies(Name=key["name"])
                    query_set.save()
                # if club does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                # intermediary table stuff
                person.save(commit = False)
                club_to_person = PersonToClubs_Hobbies(CHID=query_set, PersonID=person, Desc=key["description"])
                club_to_person.save()

        elif label == "volunteering":
            for key in js[label]:
                # check to see if volunteer exists
                query_set = Volunteering.objects.all()
                query_set = query_set.filter(Name=key["name"])
                # if volunteer does not exist create volunteer
                if not query_set:
                    query_set = Volunteering(Name=key["name"])
                    query_set.save()
                # if volunteer does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                # intermediary table stuff
                person.save(commit = False)
                volunteer_to_person = PersonToVolunteering(VolunID=query_set, PersonID=person, Desc=key["description"])
                volunteer_to_person.save()

        elif label == "course":
            for key in js[label]:
                # check to see if course exists
                query_set = Coursework.objects.all()
                query_set = query_set.filter(Name=key["name"])
                # if course does not exist create course
                if not query_set:
                    query_set = Coursework(Name=key["name"])
                    query_set.save()
                # if course does exist, grab first match from queryset
                else:
                    query_set = query_set[0]
                # intermediary table stuff
                person.save(commit = False)
                course_to_person = PersonToCourse(CourseID=query_set, PersonID=person,Desc=key["description"])
                course_to_person.save()
@login_required
def uploaddoc(request):
# Handle file upload
    if request.method == 'POST':
        form = DocumentForm()
        print(request.FILES)
        files = request.FILES.getlist('docfile')
        print("File list",files)
        for f in files:
            temp_doc = Document(docfile = f)
            temp_doc.type = request.POST['type']
            temp_doc.uploaduser = request.user.username
            temp_doc.save()
            if ".doc" in temp_doc.docfile.path:
                print (temp_doc.docfile.path)
                temp_doc.wordstr = parse_word_file(temp_doc.docfile.path)
                print (temp_doc.wordstr)
                temp_doc.save(update_fields=['wordstr'])

                ### UNCOMMENT THESE LINES FOR MAC/LINUX USERS: OCR/TEXTRACT
            else:
                temp_doc.wordstr = textract.process(temp_doc.docfile.path).decode("utf-8")
                if len(temp_doc.wordstr) < 50:
                    img=IMG(filename=temp_doc.docfile.path,resolution=200)
                    img.save(filename='temp.jpg')
                    utf8_text = get_string('temp.jpg')
                    os.remove('temp.jpg')
                    temp_doc.wordstr = utf8_text.decode("utf-8")
                    temp_doc.save(update_fields=['wordstr'])

                temp_doc.save(update_fields=['wordstr'])
            parse_back(temp_doc.wordstr,temp_doc.docfile.path,temp_doc.type)
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request,'index.html',{'documents': documents,'form':form})


#edit function
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def person_edit(request, person_id):

    instance = get_object_or_404(Person, id=person_id)
    form = PersonForm(request.POST or None, instance=instance)


    if form.is_valid():
        person = Person.objects.get(pk=person_id)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()

        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.pk]))
    context = {
    	'form' : form,
    	'pk' : person_id,
    	'person':instance
    }
    return render(request, 'person_update_form.html', context)


@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def cert_edit(request, cert_id):

    instance= get_object_or_404(PersonToCert,id=cert_id)
    form = PersontoCertForm(request.POST or None, instance=instance)
    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))
    context = {
        'form': form,
        'pk':cert_id,
        'person': instance
    }

    return render(request,'cert_update_form.html',context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def train_edit(request, train_id):

    instance= get_object_or_404(PersonToTraining,id=train_id)
    form = PersontoTrainForm(request.POST or None, instance=instance)
    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))
    context = {
        'form': form,
        'pk':train_id,
        'person': instance
    }

    return render(request,'train_update_form.html',context)


@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def skill_edit(request, skill_id):
    instance = get_object_or_404(PersonToSkills, id=skill_id)
    form = PersontoSkillForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()

        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))
    context = {
        'form': form,
        'pk':skill_id,
        'person': instance
    }
    return render(request, 'skill_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def company_edit(request, company_id):
    instance = get_object_or_404(PersonToCompany, id=company_id)
    form = PersontoCompanyForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':company_id,
        'person': instance
    }
    return render(request, 'company_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def school_edit(request, school_id):
    instance = get_object_or_404(PersonToSchool, id=school_id)
    form = PersontoSchoolForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':school_id,
        'person': instance
    }
    return render(request, 'school_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def course_edit(request, course_id):
    instance = get_object_or_404(PersonToCourse, id=course_id)
    form = PersontoCourseForm(request.POST or None, instance=instance)
    print("EDIT")
    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':course_id,
        'person': instance
    }
    return render(request, 'course_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def language_edit(request, language_id):
    instance = get_object_or_404(PersonToLanguage, id=language_id)
    form = PersontoLanguageForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':language_id,
        'person': instance
    }
    return render(request, 'language_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def sidepro_edit(request, sidepro_id):
    instance = get_object_or_404(PersonToSide, id=sidepro_id)
    form = PersontoSideForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':sidepro_id,
        'person': instance
    }
    return render(request, 'sidepro_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def award_edit(request, award_id):
    instance = get_object_or_404(PersonToAwards, id=award_id)
    form = PersontoAwardForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':award_id,
        'person': instance
    }
    return render(request, 'award_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def club_edit(request, club_id):
    instance = get_object_or_404(PersonToClubs_Hobbies, id=club_id)
    form = PersontoClubForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':club_id,
        'person': instance
    }
    return render(request, 'club_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def volunteer_edit(request, volunteer_id):
    instance = get_object_or_404(PersonToVolunteering, id=volunteer_id)
    form = PersontoVolunteeringForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':volunteer_id,
        'person': instance
    }
    return render(request, 'volunteer_update_form.html', context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def professional_edit(request,pro_id):
    instance = get_object_or_404(PersonToProfessionalDevelopment, id=pro_id)
    form = PersontoProfessionalForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':pro_id,
        'person': instance
    }
    return render(request, 'professional_update_form.html', context)

def clearance_edit(request,clearance_id):
    instance = get_object_or_404(PersonToClearance, id=clearance_id)
    form = PersontoClearanceForm(request.POST or None, instance=instance)

    if form.is_valid():
        person = Person.objects.get(pk=instance.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[instance.PersonID.pk]))

    context = {
        'form': form,
        'pk':clearance_id,
        'person': instance
    }
    return render(request, 'clearance_update_form.html', context)

#end edit

##########delete##############

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def skill_delete(request,pk,template_name='skill_update_form.html'):
    skills = get_object_or_404(PersonToSkills, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=skill.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        skills.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[skills.PersonID.pk]))
    return render(request, template_name, {'object': skills})



@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def company_delete(request,pk,template_name='detail.html'):
    company = get_object_or_404(PersonToCompany, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=company.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        company.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[company.PersonID.pk]))
    return render(request, template_name, {'object': company})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def school_delete(request,pk,template_name='detail.html'):
    school = get_object_or_404(PersonToSchool, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=school.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        school.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[school.PersonID.pk]))
    return render(request, template_name, {'object': school})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def course_delete(request,pk,template_name='detail.html'):
    course = get_object_or_404(PersonToCourse, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=course.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        course.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[course.PersonID.pk]))
    return render(request, template_name, {'object': course})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def language_delete(request,pk,template_name='detail.html'):
    language = get_object_or_404(PersonToLanguage, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=language.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        language.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[language.PersonID.pk]))
    return render(request, template_name, {'object': language})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def sidepro_delete(request,pk,template_name='detail.html'):
    sidepro = get_object_or_404(PersonToSide, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=sidepro.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        sidepro.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[sidepro.PersonID.pk]))
    return render(request, template_name, {'object': sidepro})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def award_delete(request,pk,template_name='detail.html'):
    award = get_object_or_404(PersonToAwards, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=award.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        award.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[award.PersonID.pk]))
    return render(request, template_name, {'object': award})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def club_delete(request,pk,template_name='detail.html'):
    club = get_object_or_404(PersonToClubs_Hobbies, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=club.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        club.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[club.PersonID.pk]))
    return render(request, template_name, {'object': club})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def volunteer_delete(request,pk,template_name='detail.html'):
    volunteer = get_object_or_404(PersonToVolunteering, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=volunteer.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        volunteer.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[volunteer.PersonID.pk]))
    return render(request, template_name, {'object': volunteer})

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def professional_delete(request,pk,template_name='detail.html'):
    professional = get_object_or_404(PersonToProfessionalDevelopment, pk=pk)
    if request.method == 'POST':
        person = Person.objects.get(pk=professional.PersonID.pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        professional.delete()
        return HttpResponseRedirect(reverse('RSR:detail', args=[professional.PersonID.pk]))
    return render(request, template_name, {'object': professional})

#########end delete###########





@login_required
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def detail(request,pk):
       # Get the current person object using pk or id
    person = get_object_or_404(Person, pk=pk)
    related_obj_list=Detail(person)

    detail_dic = Detail2(person)
    School_Detail = detail_dic['PersonToSchool']
    Course_Detail = detail_dic['PersonToCourse']
    Pro = detail_dic['PersonToProfessionalDevelopment']
    Side = detail_dic['PersonToSide']
    Skills_Detail = detail_dic['PersonToSkills']
    Language = detail_dic['PersonToLanguage']
    Clearance = detail_dic['PersonToClearance']
    Company_Detail = detail_dic['PersonToCompany']
    Clubs = detail_dic['PersonToClubs_Hobbies']
    Volunteer = detail_dic['PersonToVolunteering']
    Award = detail_dic['PersonToAwards']
    Certification = detail_dic['PersonToCert']
    Training = detail_dic['PersonToTraining']
    print('Certs',Certification)
    print('Training',Training)
    form = CommentsForm(request.POST or None, instance=person)


    if form.is_valid():
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        form.save()

        return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))

    print(request.POST)

    persontocertform = NewPersonToCertForm(request.POST,prefix = 'personcert')
    certform = CertForm(request.POST,prefix='cert')
    if certform.is_valid():
        print('cert',certform)
        person = Person.objects.get(pk=pk)
        person.LastUpdated =datetime.now()
        cert = certform.save()
        if persontocertform.is_valid():
            p2c = persontocertform.save(commit= False)
            p2c.PersonID = person
            p2c.Start_date = datetime.now()
            p2c.CertID = cert
            p2c.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))


    trainform= TraingingForm(request.POST,prefix='train')
    persontotrainform = NewPersonToTrainForm(request.POST,prefix = 'persontrain')

    if trainform.is_valid():
        person = Person.objects.get(pk=pk)
        person.LastUpdated =datetime.now()
        train = trainform.save()
        if persontotrainform.is_valid():
            p2t = persontotrainform.save(commit=False)
            p2t.PersonID =person
            p2t.TrainID = train
            p2t.Start_date =datetime.now()
            p2t.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))


    #add Skill
    skillform = SkillForm(request.POST)
    persontoskill = NewPersontoSkillForm(request.POST)
    if skillform.is_valid() and not skillform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        skillform.save(commit=False)
        query_set = Skills.objects.all()


        if not query_set.filter(Name=skillform.cleaned_data['Name']):
            skillform.save()
            query_set = query_set.filter(Name=skillform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=skillform.cleaned_data['Name'])[0]
        if persontoskill.is_valid():
            persontoskill_temp = persontoskill.save(commit=False)
            persontoskill_temp.SkillsID = query_set

            persontoskill_temp.PersonID = person

            persontoskill_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add skill

     #add Company
    companyform = CompanyForm(request.POST)
    persontocompany = NewPersontoCompanyForm(request.POST)
    if companyform.is_valid() and not companyform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        companyform.save(commit=False)
        query_set = Company.objects.all()


        if not query_set.filter(Name=companyform.cleaned_data['Name']):
            companyform.save()
            query_set = query_set.filter(Name=companyform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=companyform.cleaned_data['Name'])[0]
        if persontocompany.is_valid():
            persontocompany_temp = persontocompany.save(commit=False)
            persontocompany_temp.CompanyID = query_set

            persontocompany_temp.PersonID = person

            persontocompany_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add company

      #add school
    majorform = NewMajorForm(prefix = "majorform")
    schoolform = NewSchoolForm(prefix = "schoolform")

    majorform = NewMajorForm(request.POST, prefix = "majorform")
    schoolform = NewSchoolForm(request.POST, prefix = "schoolform")
    persontoschool  = NewPersontoSchoolForm(request.POST)

    if schoolform.is_valid() and not schoolform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        schoolform.save(commit=False)
        query_set = School.objects.all()


        if not query_set.filter(Name=schoolform.cleaned_data['Name']):
            schoolform.save()
            query_set = query_set.filter(Name=schoolform.cleaned_data['Name'])[0]
        else:
            query_set = query_set.filter(Name=schoolform.cleaned_data['Name'])[0]
        if majorform.is_valid():
            majorform.save(commit=False)
            query_set1 = Major.objects.all()


            if not query_set1.filter(Name=majorform.cleaned_data['Name'],MajorMinor = majorform.cleaned_data['MajorMinor']):
                majorform.save()
                query_set1 = query_set1.filter(Name=majorform.cleaned_data['Name'],MajorMinor = majorform.cleaned_data['MajorMinor'])[0]
            else:
                query_set1 = query_set1.filter(Name=majorform.cleaned_data['Name'],MajorMinor = majorform.cleaned_data['MajorMinor'])[0]

            if persontoschool.is_valid():
                persontoschool_temp = persontoschool.save(commit=False)
                persontoschool_temp.MajorID = query_set1
                persontoschool_temp.SchoolID = query_set

                persontoschool_temp.PersonID = person

                persontoschool_temp.save()
                return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add school
     #add Course
    courseform = CourseForm(prefix = "courseform")
    courseform = CourseForm(request.POST, prefix = "courseform")
    persontocourse = NewPersontoCourseForm(request.POST)
    if courseform.is_valid() and not courseform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        courseform.save(commit=False)
        query_set = Coursework.objects.all()


        if not query_set.filter(Name=courseform.cleaned_data['Name']):
            courseform.save()
            query_set = query_set.filter(Name=courseform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=courseform.cleaned_data['Name'])[0]
        if persontocourse.is_valid():
            persontocourse_temp = persontocourse.save(commit=False)
            persontocourse_temp.CourseID = query_set

            persontocourse_temp.PersonID = person

            persontocourse_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add course
    #add Lang
    langform = LanguageForm(prefix = "langform")
    langform = LanguageForm(request.POST, prefix = "langform")
    if langform.is_valid() and not langform.cleaned_data['Language'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        langform.save(commit=False)
        query_set = LanguageSpoken.objects.all()


        if not query_set.filter(Language=langform.cleaned_data['Language']):
            langform.save()
            query_set = query_set.filter(Language=langform.cleaned_data['Language'])[0]

        else:
            query_set = query_set.filter(Language=langform.cleaned_data['Name'])[0]
        language_to_person = PersonToLanguage(LangID=query_set, PersonID=person)
        language_to_person.save()
        return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add Lang

        #add Side Project
    sideform = SideForm(prefix = "sideform")
    sideform = SideForm(request.POST, prefix = "sideform")
    persontoside = NewPersontoSideForm(request.POST)
    if sideform.is_valid() and not sideform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        sideform.save(commit=False)
        query_set = SideProject.objects.all()


        if not query_set.filter(Name=sideform.cleaned_data['Name']):
            sideform.save()
            query_set = query_set.filter(Name=sideform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=sideform.cleaned_data['Name'])[0]
        if persontoside.is_valid():
            persontoside_temp = persontoside.save(commit=False)
            persontoside_temp.SideID = query_set

            persontoside_temp.PersonID = person

            persontoside_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add Project
    #add Award
    awardform = AwardForm(prefix = "awardform")
    awardform = AwardForm(request.POST, prefix = "awardform")
    persontoaward = NewPersontoAwardForm(request.POST)
    if awardform.is_valid() and not awardform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        awardform.save(commit=False)
        query_set = Awards.objects.all()


        if not query_set.filter(Name=awardform.cleaned_data['Name']):
            awardform.save()
            query_set = query_set.filter(Name=awardform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=awardform.cleaned_data['Name'])[0]
        if persontoaward.is_valid():
            persontoaward_temp = persontoaward.save(commit=False)
            persontoaward_temp.AwardID = query_set

            persontoaward_temp.PersonID = person

            persontoaward_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add award

    #add Club
    clubform = ClubForm(prefix = "clubform")
    clubform = ClubForm(request.POST, prefix = "clubform")
    persontoclub = NewPersontoClubForm(request.POST)
    if clubform.is_valid() and not clubform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        clubform.save(commit=False)
        query_set = Clubs_Hobbies.objects.all()


        if not query_set.filter(Name=clubform.cleaned_data['Name']):
            clubform.save()
            query_set = query_set.filter(Name=clubform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=clubform.cleaned_data['Name'])[0]
        if persontoclub.is_valid():
            persontoclub_temp = persontoclub.save(commit=False)
            persontoclub_temp.CHID = query_set

            persontoclub_temp.PersonID = person

            persontoclub_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add club


     #add volunteer
    volunteerform = VolunteeringForm(prefix = "volunteerform")
    volunteerform = VolunteeringForm(request.POST, prefix = "volunteerform")
    persontovolunteer = NewPersontoVolunteerForm(request.POST)
    if volunteerform.is_valid() and not volunteerform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        volunteerform.save(commit=False)
        query_set = Volunteering.objects.all()


        if not query_set.filter(Name=volunteerform.cleaned_data['Name']):
            volunteerform.save()
            query_set = query_set.filter(Name=volunteerform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=volunteerform.cleaned_data['Name'])[0]
        if persontovolunteer.is_valid():
            persontovolunteer_temp = persontovolunteer.save(commit=False)
            persontovolunteer_temp.VolunID = query_set

            persontovolunteer_temp.PersonID = person

            persontovolunteer_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add volunteer

     #add Professional
    professionalform = ProfessionalForm(prefix = "professionalform")
    professionalform = ProfessionalForm(request.POST, prefix = "professionalform")
    persontoprofessional = NewPersontoProfessionalForm(request.POST)
    if professionalform.is_valid() and not professionalform.cleaned_data['Name'] == "":
        person = Person.objects.get(pk=pk)
        print(person)
        person.LastUpdated = datetime.now()
        person.save(update_fields=['LastUpdated'])
        professionalform.save(commit=False)
        query_set = ProfessionalDevelopment.objects.all()


        if not query_set.filter(Name=professionalform.cleaned_data['Name']):
            professionalform.save()
            query_set = query_set.filter(Name=professionalform.cleaned_data['Name'])[0]

        else:
            query_set = query_set.filter(Name=professionalform.cleaned_data['Name'])[0]
        if persontoprofessional.is_valid():
            persontoprofessional_temp = persontoprofessional.save(commit=False)
            persontoprofessional_temp.ProfID = query_set

            persontoprofessional_temp.PersonID = person

            persontoprofessional_temp.save()
            return HttpResponseRedirect(reverse('RSR:detail', args=[person.pk]))
    ## end add club
    context = {
                'form' : form,
                'skillform': skillform,
                'majorform':majorform,
                'schoolform':schoolform,
                'persontoschool':persontoschool,
                'companyform':companyform,
                'courseform':courseform,
                'persontocourse':persontocourse,
                'persontocompany':persontocompany,
                'persontoskill':persontoskill,
                'person':person,
                'list': related_obj_list,
                'school':School_Detail,
                'course':Course_Detail,
                'pro':Pro,
                'professionalform':professionalform,
                'persontoprofessional':persontoprofessional,
                'side':Side,
                'sideform':sideform,
                'persontoside':persontoside,
                'skills':Skills_Detail,
                'language':Language,
                'langform':langform,
                'clearance':Clearance,
                'company':Company_Detail,
                'clubs':Clubs,
                'clubform':clubform,
                'persontoclub':persontoclub,
                'volunteer':Volunteer,
                'volunteerform':volunteerform,
                'persontovolunteer':persontovolunteer,
                'award':Award,
                'awardform':awardform,
                'persontoaward':persontoaward,
                'training':Training,
                'certs':Certification,
                'certform':certform,
                'trainform':trainform,
                'persontocertform':persontocertform,
                'persontotrainform':persontotrainform,
                }

    return render(request, 'SearchExport/detail.html', context)




@login_required
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def uploadlist (request):
   # documents = Document.objects.filter(firstname = Document.firstname).filter(lastname = Document.lastname).filter(type = Document.type).filter(docfile = Document.docfile)
    document = Document.objects.all()
    documents = UploadListFilter(request.GET,queryset = document)

    context ={'documents':documents}
    return render(request,'uploadlist.html',context)

@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def listdelete(request, template_name='uploadlist.html'):
    docId = request.POST.get('docfile', None)
    documents = get_object_or_404(Document, pk=docId)
    if request.method == 'POST':


        documents.delete()
        return HttpResponseRedirect(reverse('RSR:uploadlist'))

    return render(request, template_name, {'object': documents})

def parse_word_file(filepath):
	parsed_string = docx2txt.process(filepath)
	return parsed_string



# SEARCH/EXPORT TEAM
@login_required
@user_passes_test(lambda u: u.groups.filter(name='RSR').exists())
def search(request):
    arr = []
    print(request.GET)
    print('test',Person.objects.filter(persontoschool__SchoolID = 29))
    query_set = Person.objects.order_by('Name').distinct()
    personFilter = PersonFilter(request.GET, query_set)
    print(personFilter.qs)
    print('form',personFilter.form)
    print(personFilter.form.errors)
    if len(request.GET) != 0:
        if request.GET.get('Skills', '')!='' and request.GET.get('YearOfExperienceForSkill', '')!='':
            for p in personFilter.qs:
                if len(PersonToSkills.objects.filter(PersonID = p.pk)\
                    .filter(SkillsID =request.GET.get('Skills', ''))\
                    .filter(YearsOfExperience = request.GET.get('YearOfExperienceForSkill', ''))) !=0:
                    arr.append(p)
        print('ARR',arr)
    if len(arr)  == 0:
        arr = list(personFilter.qs)
    return render(request, 'SearchExport/search.html', {'personFilter': personFilter,'qs':arr})

class TrainingAutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for ProfessionalDevelopment class
    def get_queryset(self):
        qs = Trainings.objects.all().order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs

class CertificationAutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for ProfessionalDevelopment class
    def get_queryset(self):
        qs = Certifications.objects.all().order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs


class SchoolAutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for ProfessionalDevelopment class
    def get_queryset(self):
        qs = School.objects.all().order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        print(qs)
        return qs


class ProfessionalDevelopmentAutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for ProfessionalDevelopment class
    def get_queryset(self):
        qs = ProfessionalDevelopment.order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs

class NameAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		#qs = Intern.objects.order_by('FName').distinct()
		qs = Person.objects.all()
		if self.q:
		#qs = qs.filter(FName__exact='Sam')

			qs = (qs.filter(Name__icontains=self.q))
		return qs
class Skillsutocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Skills class
    def get_queryset(self):
        qs = Skills.objects.order_by('Name').distinct()

        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs

class Volunteeringautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Volunteering class
    def get_queryset(self):
        qs = Volunteering.objects.order_by('Name').distinct()
        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs

class Languageautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for LanguageSpoken class
    def get_queryset(self):
        qs = LanguageSpoken.objects.order_by('Language').distinct()
        if self.q:
            qs = qs.filter(Language__icontains=self.q)
        return qs

class Companyautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Company class
    def get_queryset(self):
        qs = Company.objects.order_by('Name').distinct()
        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs

class Courseworkautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Coursework class
    def get_queryset(self):
        qs = PersonToCourse.objects.order_by('Desc').distinct()
        if self.q:
            qs = qs.filter(Desc__icontains=self.q)
        return qs

class Awardsautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Awards class
    def get_queryset(self):
        qs = Awards.objects.order_by('Name').distinct()
        if self.q:
            qs = qs.filter(Name__icontains=self.q)
        return qs

class Titleautocomplete(autocomplete.Select2QuerySetView):
    # autocomplete function for Title class
    def get_queryset(self):
        qs = PersonToCompany.objects.order_by('Title').distinct()
        if self.q:
            qs = qs.filter(Title__icontains=self.q)
        return qs

    def get_result_label(self, item):
        return item.Title

    def get_result_value(self, item):
        return item.Title
#OCR's Search. REGEX ON RESUME TEXT

def OCRSearch(request):
    doc_objects = Document.objects.all()
    search_item = str(request.GET.get('search'))
    # print(search_item)
    results=[]
    for document in doc_objects:
        # print(document.wordstr)
        wordstr = str(document.wordstr)
        if search_item.lower() in wordstr.lower():
            # print(document.wordstr)
            results.append(document)
    context = {'results': results}

    return render(request, 'OCRSearch.html', context)
