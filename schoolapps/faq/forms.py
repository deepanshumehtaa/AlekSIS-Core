from django import forms

class FAQForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(),
                               label='Bitte gib deine Frage hier ein', required=True)