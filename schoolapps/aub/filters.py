from django import forms
from django.contrib.auth.models import User
import django_filters
from .models import Aub


class AUBFilter(django_filters.FilterSet):
    def getAUBUsers():
        ''' Find all users who sends an AUB'''
        aub_users = Aub.objects.values_list('created_by')
        users = list(User.objects.filter(id__in=aub_users))
        # user_ids = [(str(user.id),user.username) for user in users]
        user_ids = [(str(user.id),user.last_name+', '+user.first_name) for user in users]
        user_ids_sorted = sorted(user_ids, key=lambda user: user[1])
        return user_ids_sorted

    created_by = django_filters.ChoiceFilter(label='Von', choices=getAUBUsers())

    class Meta:
        model = Aub
        fields = ['created_by',]

