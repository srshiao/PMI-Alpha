from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.http import Http404
from django.forms import ModelForm
#from .models import PersonForm
from .forms import *
from .tables import WorkTable
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import TemplateView
from django_tables2 import SingleTableView
import datetime

from django.contrib.auth import logout

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/clockin/')


# Create your views here.

#Don't worry about this one. 
def index(request):
	table = WorkTable(Work.objects.all())
	context = {
		'table': table,

	}

	RequestConfig(request).configure(table)
	return render(request, 'ogdb/person_list.html', context)

#TGENERATES MAIN PAGE. TABLE. 
@login_required
def work_list(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/clockin/adminhome')
	filter = Work.objects.filter(user=request.user).filter(active_session=True)

	intern_obj = Intern.objects.filter(username = request.user)
	name = intern_obj[0]
	context = {
		'filter':filter,
		'name' : name,
	}

###
	if request.POST.get('mybtn'):
			ch = request.POST.get('checkbox','')
			if not ch == '':
				url = reverse_lazy ('item_edit', kwargs = {'work_id':ch})
				return HttpResponseRedirect(url)
###


	return render(request, 'ogdb/person_list.html', context)

@login_required
def past_time(request):
	filter1 = Work.objects.filter(user=request.user).filter(active_session=False)

	intern_obj = Intern.objects.filter(username = request.user)
	name = intern_obj[0]
	context = {
		'filter1':filter1,
		'name' : name,
	}

###
###
	return render(request, 'ogdb/past_time.html', context)

#not in current use. will be used as a Constituent Details Page
@login_required
def detail(request, work_id):
	try:
		person = Work.objects.get(pk=work_id)
	except Work.DoesNotExist:
		raise Http404("Log does not exist")
	return render(request, 'ogdb/detail.html', {'employee': person})

@login_required
def add_new(request):
	form = ClockinForm(request.POST or None);
	context = {
		'form' : form
	}
	if form.is_valid():
		obj = form.save(commit=False)
		intern_obj = Intern.objects.filter(username = request.user)
		obj.intern = intern_obj[0]
		obj.time_in = datetime.datetime.now().time()
		obj.active_session = True
		obj.user = request.user
		obj.duration = 0
		obj.save()
		return HttpResponseRedirect('/clockin/')


	return render(request, 'ogdb/new_person.html', context)

@login_required
def clockout(request, work_id):
	instance = get_object_or_404(Work, id=work_id)
	form = ClockoutForm(request.POST or None, instance=instance)
   

	if form.is_valid():
		obj = form.save(commit=False)
		obj.time_out = datetime.datetime.now().time()
		obj.active_session = False
		my_date = datetime.date.today()

		delta = datetime.datetime.combine(my_date,obj.time_out) - datetime.datetime.combine(my_date,obj.time_in)
		totalseconds = delta.total_seconds()
		hours = totalseconds/3600
		if hours > 12:
			obj.duration = 12
		else:
			obj.duration = hours
		obj.save()
		return HttpResponseRedirect('/clockin/')
	context = {
		'form' : form,
		'pk' : work_id
	}

    
	return render(request, 'ogdb/item_edit.html', context)


#Delete Person confirm page
class workDelete(DeleteView):
	model = WorkForm
	success_url = reverse_lazy('home')
	template_name = 'ogdb/person_confirm_delete.html'

from .filters import WorkListFilter
from .forms import WorkListFormHelper

class WorkListView(TemplateView):
    template_name = 'ogdb/person_list_2.html'

    def get_queryset(self, **kwargs):
        return Work.objects.all()

    def get_context_data(self, **kwargs):
        context = super(WorkListView, self).get_context_data(**kwargs)
        filter = WorkListFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = WorkListFormHelper()
        table = WorkTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context

@login_required
def AdminView(request):
	if not request.user.is_superuser:
		return HttpResponseRedirect('/clockin/')
	f = WorkListFilter(request.GET,queryset = Work.objects.all())
	table = WorkTable(Work.objects.all())
	table.exclude = ('id',)
	context = {
		'table': table,
		'filter': f,
	}

	RequestConfig(request).configure(table)
	return render(request, 'ogdb/datefilter.html', context)




