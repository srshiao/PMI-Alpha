import django_filters
from .models import Work


class WorkListFilter(django_filters.FilterSet):
	date_between = django_filters.DateFromToRangeFilter(name='date',label='Date (Between)', widget=django_filters.widgets.RangeWidget())

	class Meta:
		model = Work
		fields =  ('intern',)
		order_by = ['pk']