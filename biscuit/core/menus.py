from django.conf import settings
from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Account"),
            "url": "#",
            "root": True,
            "submenu": [
                {
                    "name": _("Stop impersonation"),
                    "url": "impersonate-stop",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "biscuit.core.util.core_helpers.is_impersonate",
                    ],
                },
                {
                    "name": _("Login"),
                    "url": settings.LOGIN_URL,
                    "validators": ["menu_generator.validators.is_anonymous"],
                },
                {
                    "name": _("Logout"),
                    "url": "logout",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Two factor auth"),
                    "url": "two_factor:profile",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        lambda request: "two_factor" in settings.INSTALLED_APPS,
                    ],
                },
            ],
        },
        {
            "name": _("Admin"),
            "url": "#",
            "validators": [
                "menu_generator.validators.is_authenticated",
                "menu_generator.validators.is_superuser",
            ],
            "submenu": [
                {
                    "name": _("Data management"),
                    "url": "data_management",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "menu_generator.validators.is_superuser",
                    ],
                },
                {
                    "name": _("System status"),
                    "url": "system_status",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "menu_generator.validators.is_superuser",
                    ],
                },
                {
                    "name": _("Impersonation"),
                    "url": "impersonate-list",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "menu_generator.validators.is_superuser",
                    ],
                },
                {
                    "name": _("Manage school"),
                    "url": "school_management",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "menu_generator.validators.is_superuser",
                    ],
                },
                {
                    "name": _("Settings"),
                    "url": "site_settings",
                    "icon": "settings",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "menu_generator.validators.is_superuser",
                    ],
                },
            ],
        },
        {
            "name": _("People"),
            "url": "#",
            "root": True,
            "validators": [
                "menu_generator.validators.is_authenticated",
                "biscuit.core.util.core_helpers.has_person",
            ],
            "submenu": [
                {
                    "name": _("Persons"),
                    "url": "persons",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Groups"),
                    "url": "groups",
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Persons and accounts"),
                    "url": "persons_accounts",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "menu_generator.validators.is_superuser",
                    ],
                },
            ],
        },
    ],
    "FOOTER_MENU_CORE": [
        {
            "name": _("BiscuIT Software"),
            "url": "#",
            "submenu": [
                {"name": _("Website"), "url": "https://biscuit.edugit.io/"},
                {"name": "Teckids e.V.", "url": "https://www.teckids.org/"},
            ],
        },
    ],
    "DATA_MANAGEMENT_MENU": [],
    "SCHOOL_MANAGEMENT_MENU": [
        {"name": _("Edit school information"), "url": "edit_school_information",},
        {"name": _("Edit school term"), "url": "edit_school_term",},
    ],
}
