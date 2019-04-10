from django import forms
from django.contrib.auth.models import User
import django_filters
from .models import Aub


class AUBFilter(django_filters.FilterSet):
    def getAUBUsers():
        ''' Find all users who sends an AUB'''
        aub_users = Aub.objects.values_list('created_by')
        users = list(User.objects.filter(id__in=aub_users))
        user_ids = [(str(user.id),user.username) for user in users]
        return user_ids

    created_by = django_filters.ChoiceFilter(label='Von', choices=getAUBUsers())

    class Meta:
        model = Aub
        fields = ['created_by',]

