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
    ratings = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

    design_rating = forms.ChoiceField(label="Design",
                                      choices=ratings,
                                      widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                      required=True,
                                      )

    performance_rating = forms.ChoiceField(label='Geschwindigkeit',
                                           choices=ratings,
                                           widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                           required=True)

    usability_rating = forms.ChoiceField(label='Benutzerfreundlichkeit',
                                         choices=ratings,
                                         widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                         required=True)

    overall_rating = forms.ChoiceField(label='SchoolApps allgemein',
                                       choices=ratings,
                                       widget=forms.RadioSelect(attrs={"checked": "checked"}),
                                       required=True)

    apps = forms.CharField(
        label="Bitte sage uns, was dir an SchoolApps gefällt und was dich stört bzw. was du ändern würdest.",
        required=False,
        widget=forms.Textarea)

    more = forms.CharField(label="Möchtest du uns sonst noch etwas mitteilen?",
                           required=False,
                           widget=forms.Textarea(
                               attrs={"class": "materialize-textarea"}
                           ))
    ideas = forms.CharField(
        label='Hast du Ideen, was wir noch in SchoolApps einbauen könnten/sollten?',
        required=False,
        widget=forms.Textarea)
