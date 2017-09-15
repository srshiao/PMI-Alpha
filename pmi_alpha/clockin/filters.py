import django_filters
from .models import Work


class WorkListFilter(django_filters.FilterSet):
	date_between = django_filters.DateFromToRangeFilter(name='date',label='Pay Period (MM/DD/YY)', widget=django_filters.widgets.RangeWidget())

	class Meta:
		model = Work
		fields =  ('intern',)
<<<<<<< HEAD
<<<<<<< HEAD
		order_by = ['intern__FName']
=======
		order_by = ['pk']
>>>>>>> ded216f852c651889e7872ae31f367c57d02966f
=======
		order_by = ['intern__FName']
>>>>>>> 903f24b60272e7eaa88f16e6d4c4b0817793b9ab
