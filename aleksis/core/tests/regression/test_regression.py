def test_all_settigns_registered():
    """Tests for regressions of preferences not being registered.

    https://edugit.org/AlekSIS/official/AlekSIS-Core/-/issues/592
    """

    from dynamic_preferences.types import BasePreferenceType

    from aleksis.core import preferences
    from aleksis.core.preferences import person_preferences_registry, site_preferences_registry

    for obj in preferences.__dict__.values():
        if not isinstance(obj, BasePreferenceType):
            continue

        in_site_reg = site_preferences_registry.get(obj.section.name, {}).get(obj.name, None) is obj
        in_person_reg = (
            person_preferences_registry.get(obj.section.name, {}).get(obj.name, None) is obj
        )

        assert in_site_reg != in_person_reg
