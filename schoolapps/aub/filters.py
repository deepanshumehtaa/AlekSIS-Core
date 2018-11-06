from django import forms
import django_filters
from .models import Aub

class AUBFilter(django_filters.FilterSet):
    #timerangechoices = [('today','Heute'),('thisWeek','Diese Woche'), ('thisMonth','Dieser Monat')]
    #timerange = django_filters.ChoiceFilter(label='Zeitumfang', choices=timerangechoices)
    created_by = django_filters.ChoiceFilter(label='Von')
    statuschoices = [('1','In Bearbeitung 1'),('2','In Bearbeitung 2'),('3','Genehmigt'),('4','Abgelehnt')]
    status = django_filters.ChoiceFilter(label='Status', choices=statuschoices, initial='In Bearbeitung 1')
    class Meta:
        model = Aub
        fields = [ 'created_by', 'status']
        ordering = 'status'