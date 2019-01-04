from django import forms
from material import Layout, Row, Fieldset


class REBUSForm(forms.Form):
    categories = [('Kein WLAN', 'Kein WLAN'), ('Beamer funktioniert nicht', 'Beamer funktioniert nicht'), ('Fernseher funktioniert nicht', 'Fernseher funktioniert nicht'),
                  ('PC funktioniert nicht', 'PC funktioniert nicht'), ('Laptop funktioniert nicht', 'Laptop funktioniert nicht'), ('Sonstiges', 'Sonstiges')]

    room = forms.CharField(label='Ihr Raum', max_length=15, required=True)
    contraction = forms.CharField(label='Ihr Kürzel', max_length=10, required=True)
    category = forms.ChoiceField(label='Kategorie', choices=categories, required=True)
    short_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler in einem Satz', required=True)
    long_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler genauer', required=False)

    layout = Layout(Row('room', 'contraction', 'category'),
                    Row('short_description'),
                    Row('long_description'),
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

    layout = Layout(Row('category'),
                    Row('short_description'),
                    Row('long_description'),
                    Row('rating'),
                    )
