from django import forms
from material import Layout, Row, Fieldset


class REBUSForm(forms.Form):
    a = forms.CharField(label="Kategorie A", required=True)
    b = forms.CharField(label="Kategorie B", required=False)
    c = forms.CharField(label="Kategorie C", required=False)
    short_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler in einem Satz', required=True)
    long_description = forms.CharField(widget=forms.Textarea, label='Bitte beschreiben Sie Ihren Fehler genauer',
                                       required=False)


class FeedbackForm(forms.Form):
    ratings = [(1, 1), (2, 2), (3, 3),
               (4, 4), (5, 5), (6, 6),
               (7, 7), (8, 8), (9, 9),
               (10, 10)]

    design_rating = forms.ChoiceField(label='Bitte bewerte das Design von SchoolApps auf einer Skala von 1 bis 10',
                                      choices=ratings, required=True)
    performance_rating = forms.ChoiceField(label='Bitte bewerte die Geschwindigkeit von SchoolApps auf einer '
                                                 'Skala von 1 bis 10',
                                           choices=ratings, required=True)
    usability_rating = forms.ChoiceField(label='Bitte bewerte die Benutzerfreundlichkeit von SchoolApps auf '
                                               'einer Skala von 1 bis 10',
                                         choices=ratings, required=True)
    overall_rating = forms.ChoiceField(label='Bitte bewerte SchoolApps insgesamt auf einer Skala von 1 bis 10',
                                       choices=ratings, required=True)

    apps = forms.CharField(label="Bitte gebe uns Feedback zu den einzelnen Funktionen von SchoolApps", required=False,
                           widget=forms.Textarea)
    more = forms.CharField(label="Möchtest du uns sonst noch etwas mitteilen?", required=False, widget=forms.Textarea)
    ideas = forms.CharField(label='Hast du Ideen, was wir noch in SchoolApps einbauen könnten/sollten?',
                            required=False, widget=forms.Textarea)

    layout = Layout(Row('design_rating', 'performance_rating', 'usability_rating'),
                    Row('overall_rating'),
                    Row("apps"),
                    Row('ideas'),
                    Row('more'),
                    )
