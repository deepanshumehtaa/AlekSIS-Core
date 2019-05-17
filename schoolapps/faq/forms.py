from django import forms

class FAQForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(),
                               label='Bitte geben sie ihre Frage hier ein…', required=True)