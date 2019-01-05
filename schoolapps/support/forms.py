from django import forms
from material import Layout, Row, Fieldset


class REBUSForm(forms.Form):
    categories = [('Kein WLAN', 'Kein WLAN'), ('Beamer funktioniert nicht', 'Beamer funktioniert nicht'), ('Fernseher funktioniert nicht', 'Fernseher funktioniert nicht'),
                  ('PC funktioniert nicht', 'PC funktioniert nicht'), ('Laptop funktioniert nicht', 'Laptop funktioniert nicht'), ('Sonstiges', 'Sonstiges')]

    room = forms.CharField(label='Ihr Raum', max_length=15, required=True)
    category = forms.ChoiceField(label='Kategorie', choices=categories, required=True)
    short_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler in einem Satz', required=True)
    long_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler genauer', required=False)

    layout = Layout(Row('room', 'category'),
                    Row('short_description'),
                    Row('long_description'),
                    )


class FeedbackForm(forms.Form):

    ratings = [('1', '1'), ('2', '2'), ('3', '3'),
               ('4', '4'), ('5', '5'), ('6', '6'),
               ('7', '7'), ('8', '8'), ('9', '9'),
               ('10', '10')]

    design_rating = forms.ChoiceField(label='Bitte bewerten Sie das Design der SchoolApps auf einer Skala von 1 bis 10',
                               choices=ratings, required=True)
    functions_rating = forms.ChoiceField(label='Bitte bewerten Sie die Funktionen der SchoolApps auf einer Skala von '
                                               '1 bis 10',
                               choices=ratings, required=True)
    performance_rating = forms.ChoiceField(label='Bitte bewerten Sie die Geschwindigkeit der SchoolApps auf einer '
                                                 'Skala von 1 bis 10',
                               choices=ratings, required=True)
    compatibility_rating = forms.ChoiceField(label='Bitte bewerten Sie die Kompatibilität der SchoolApps auf einer '
                                                   'Skala von 1 bis 10',
                               choices=ratings, required=True)
    usability_rating = forms.ChoiceField(label='Bitte bewerten Sie die Benutzerfreundlichkeit der SchoolApps auf '
                                               'einer Skala von 1 bis 10',
                               choices=ratings, required=True)
    overall_rating = forms.ChoiceField(label='Bitte bewerten Sie die SchoolApps insgesamt auf einer Skala von 1 bis 10',
                               choices=ratings, required=True)
    short_description = forms.CharField(label='Bitte geben Sie ein kurzes Feedback in einem Satz ein', required=True)
    long_description = forms.CharField(label='Bitte geben Sie ein ausführliches Feedback ein', required=False)

    layout = Layout(Row('design_rating'),
                    Row('functions_rating'),
                    Row('performance_rating'),
                    Row('compatibility_rating'),
                    Row('usability_rating'),
                    Row('overall_rating'),
                    Row('short_description'),
                    Row('long_description'),
                    )
