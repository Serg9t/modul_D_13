import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    date = django_filters.DateFilter(field_name='created',
                                     lookup_expr='gt',
                                     label='Date',
                                     widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'type_category': ['exact'],
            'created': ['gt'],
        }
