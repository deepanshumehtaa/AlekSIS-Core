from django import forms
from django.contrib.auth.models import User
import django_filters
from .models import Aub, Status


class AUBFilter(django_filters.FilterSet):
    def getAUBUsers():
        aub_users = Aub.objects.values_list('created_by')
        users = list(User.objects.filter(id__in=aub_users))
        user_ids = [(i+1,user.username) for i,user in enumerate(users)]
        return user_ids

    def get_status_choices():
        status_values = list(Status.objects.values_list('name'))
        status_ids = [(i+1,name[0]) for i,name in enumerate(status_values)]
        return status_ids
    print('status_values:', get_status_choices())
    print('users', getAUBUsers())
    #timerangechoices = [('today','Heute'),('thisWeek','Diese Woche'), ('thisMonth','Dieser Monat')]
    #timerange = django_filters.ChoiceFilter(label='Zeitumfang', choices=timerangechoices)
    created_by = django_filters.ChoiceFilter(label='Von', choices=getAUBUsers())
    status_choices = [('1','In Bearbeitung 1'),('2','In Bearbeitung 2'),('3','Genehmigt'),('4','Abgelehnt')]
    status = django_filters.ChoiceFilter(label='Status', choices=get_status_choices(), initial='In Bearbeitung 1')
    class Meta:
        model = Aub
        fields = [ 'created_by', 'status']
        ordering = 'status'

