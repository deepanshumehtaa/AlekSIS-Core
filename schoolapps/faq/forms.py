from django import forms

class FAQForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(),
                               label='Deine Frage', required=True)
