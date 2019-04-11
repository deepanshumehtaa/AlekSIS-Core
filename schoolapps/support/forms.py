from django import forms


class REBUSForm(forms.Form):
    a = forms.CharField(label="Kategorie A", required=True)
    b = forms.CharField(label="Kategorie B", required=False)
    c = forms.CharField(label="Kategorie C", required=False)
    short_description = forms.CharField(label='Bitte beschreiben Sie Ihren Fehler in einem Satz', required=True)
    long_description = forms.CharField(widget=forms.Textarea, label='Bitte beschreiben Sie Ihren Fehler genauer',
                                       required=False)


class FeedbackForm(forms.Form):
    ratings = [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]

    design_rating = forms.ChoiceField(label="Design der Oberfläche",
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
        label="Was gefällt Dir an SchoolApps? Was würdest du ändern?",
        required=False,
        widget=forms.Textarea)

    more = forms.CharField(
        label="Möchtest Du uns sonst noch etwas mitteilen?",
        required=False,
        widget=forms.Textarea)

    ideas = forms.CharField(
        label='Hast Du Ideen, was wir noch in SchoolApps einbauen sollten?',
        required=False,
        widget=forms.Textarea)
