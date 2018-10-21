from django import forms
import django_filters
from .models import Aub

class AUBFilter(django_filters.FilterSet):
    timerangechoices = [('today','Heute'),('thisWeek','Diese Woche'), ('thisMonth','Dieser Monat')]
    timerange = django_filters.ChoiceFilter(label='Zeitumfang', choices=timerangechoices)
    class Meta:
        model = Aub
        fields = [ 'created_at', 'created_by', 'status']
