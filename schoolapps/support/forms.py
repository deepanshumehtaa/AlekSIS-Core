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
                             'short_description'),
                    Fieldset('',
                             'long_description'),
                    )


class FeedbackForm(forms.Form):
    categories = [('1', 'Design/Benutzererlebnis'), ('2', 'Funktionen'),
                  ('3', 'Performance/Geschwindigkeit'), ('4', 'Kompatibilität'),
                  ('5', 'Verständlichkeit'), ('s', 'Sonstiges')]

    ratings = [('1', '1'), ('2', '2'), ('3', '3'),
               ('4', '4'), ('5', '5'), ('6', '6'),
               ('7', '7'), ('8', '8'), ('9', '9'),
               ('10', '10')]

    category = forms.MultipleChoiceField(label='Kategorie', choices=categories, required=True)
    short_description = forms.CharField(label='Bitte geben Sie ein Feedback in einem Satz ein', required=True)
    long_description = forms.CharField(label='Bitte geben Sie ein ausführliches Feedback ein', required=False)
    rating = forms.ChoiceField(label='Bitte bewerten Sie die SchoolApps auf einer Skala von 1 bis 10',
                               choices=ratings, required=True)

    layout = Layout(Fieldset('',
                             'category'),
                    Fieldset('',
                             'short_description'),
                    Fieldset('',
                             'long_description'),
                    Fieldset('',
                             'rating'),
                    )
