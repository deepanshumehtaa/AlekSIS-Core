from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Person


class PersonAccountForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'user']

    last_name = forms.CharField(disabled=True)
    first_name = forms.CharField(disabled=True)
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    new_user = forms.CharField(required=False)

    def clean(self) -> None:
        User = get_user_model()

        if self.cleaned_data.get('new_user', None):
            if self.cleaned_data.get('user', None):
                self.add_error('new_user', _('You cannot set a new username when also selecting an existing user.'))
            elif User.objects.filter(username=self.cleaned_data['new_user']).exists():
                self.add_error('new_user', _('This username is already in use.'))
            else:
                new_user_obj = User.objects.create_user(self.cleaned_data['new_user'],
                                                        self.instance.email,
                                                        first_name=self.instance.first_name,
                                                         last_name=self.instance.last_name)

                self.cleaned_data['user'] = new_user_obj


PersonsAccountsFormSet = forms.modelformset_factory(
    Person, form=PersonAccountForm, max_num=0, extra=0)
