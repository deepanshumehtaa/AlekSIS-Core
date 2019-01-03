from django import forms
from material import Layout, Row, Fieldset

class REBUSForm(forms.Form):
    categories = [('n1', 'Kein WLAN'), ('h1a', 'Beamer funktioniert nicht'), ('h1b', 'Fernseher funktioniert nicht'),
                  ('h2a', 'PC funktioniert nicht'), ('h2b', 'Laptop funktioniert nicht'), ('s', 'Sonstiges')]

    room = forms.CharField(label='Ihr Raum', max_length=10, required=True)
    category = forms.ChoiceField(label='Kategorie', choices=categories, required=True)
    short_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler in einem Satz', required=True)
    long_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler genauer', required=False)

    layout = Layout(Fieldset('',
                             Row('room', 'category'),
                             ),
                    Fieldset('',
                             Row('short_description'),
                             ),
                    Fieldset('',
                             'long_description'),
                    )