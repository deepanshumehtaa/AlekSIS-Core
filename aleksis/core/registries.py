from dynamic_preferences.registries import PerInstancePreferenceRegistry


class SitePreferenceRegistry(PerInstancePreferenceRegistry):
    pass


class PersonPreferenceRegistry(PerInstancePreferenceRegistry):
    pass


class GroupPreferenceRegistry(PerInstancePreferenceRegistry):
    pass


site_preferences_registry = SitePreferenceRegistry()
person_preferences_registry = PersonPreferenceRegistry()
group_preferences_registry = GroupPreferenceRegistry()
