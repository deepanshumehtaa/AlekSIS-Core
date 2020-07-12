Materialize templates
======================

AlekSIS frontend uses with the `MaterializeCSS`_ framework.

Internationalization
--------------------

Load the ``i18n`` template tag and start translating strings in templates with
the following template tags::

    {% blocktrans %}String{% endblocktrans %}
    {% trans "String" %}

``{% blocktrans %}`` is mostly used for multiple words or multiline, while ``{%
trans %}`` is used for single words.

Title and headlines
-------------------

To add a main headline or browser title to your template, you can add the
following blocks to your template::

    {% block browser_title %}Title{% endblock %}
    {% block page_title %}Headline{% endblock %}

Forms in templates
------------------

The django MaterializeCSS integrations provides support for forms in
template.

You just have to load the ``material_form`` templatetag in the ``{% load %}``
block.

The following snippet generates the form::

    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {% form form=form %}{% endform %}
        {% include "core/partials/save_button.html" %}
    </form>

``{% include "core/partials/save_button.html" %}`` includes a template snippet
from AlekSIS core.  You can modify the buttons icon and translatable caption
like this::

    {% trans "Edit" as caption %}
    {% include "core/partials/save_button.html" with caption=caption, icon="person" %}


In your ``forms.py`` you can configure the layout of the fields like in the EditPersonForm::

    class EditPersonForm(ExtensibleForm):
    """Form to edit an existing person object in the frontend."""

    layout = Layout(
        Fieldset(
            _("Base data"),
            "short_name",
            Row("user", "primary_group"),
            "is_active",
            Row("first_name", "additional_name", "last_name"),
        ),
        Fieldset(_("Address"), Row("street", "housenumber"), Row("postal_code", "place")),
        Fieldset(_("Contact data"), "email", Row("phone_number", "mobile_number")),
        Fieldset(
            _("Advanced personal data"), Row("sex", "date_of_birth"), Row("photo"), "guardians",
        ),
    )


.. _MaterializeCSS: https://materializecss.com/
