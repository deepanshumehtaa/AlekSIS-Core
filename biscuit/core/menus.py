from django.utils.translation import ugettext_lazy as _

MENUS = {
    'NAV_MENU_CORE': [
        {
            'name': _('Account'),
            'url': '#',
            'root': True,
            'submenu': [
                {
                    'name': _('Login'),
                    'url': 'login',
                    'validators': ['menu_generator.validators.is_anonymous']
                },
                {
                    'name': _('Logout'),
                    'url': 'logout',
                    'validators': ['menu_generator.validators.is_authenticated']
                }
            ]
        },
        {
            'name': _('Admin'),
            'url': '#',
            'validators': ['menu_generator.validators.is_authenticated', 'menu_generator.validators.is_superuser'],
            'submenu': [
                }
                    'name': _('Data management'),
                    'url': 'data_management',
                    'validators': ['menu_generator.validators.is_authenticated', 'menu_generator.validators.is_superuser']
                }
            ]
        },
        {
            'name': _('People'),
            'url': '#',
            'root': True,
            'submenu': [
                {
                    'name': _('Persons'),
                    'url': 'persons',
                    'validators': ['menu_generator.validators.is_authenticated']
                },
                {
                    'name': _('Groups'),
                    'url': 'groups',
                    'validators': ['menu_generator.validators.is_authenticated']
                },
                {
                    'name': _('Persons and accounts'),
                    'url': 'persons_accounts',
                    'validators': ['menu_generator.validators.is_authenticated', 'menu_generator.validators.is_superuser']
                }
            ]
        }
    ],
    'FOOTER_MENU_CORE': [
        {
            'name': _('BiscuIT Software'),
            'url': '#',
            'submenu': [
                {
                    'name': _('Website'),
                    'url': 'https://biscuit.edugit.org/'
                },
                {
                    'name': 'Teckids e.V.',
                    'url': 'https://www.teckids.org/'
                }
            ]
        }
    ],
    'DATA_MANAGEMENT_MENU': [
    ]
}
