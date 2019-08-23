MENUS = {
    'NAV_MENU_CORE': [
        {
            'name': 'Login',
            'url': 'login',
            'validators': ['menu_generator.validators.is_anonymous']
        },
        {
            'name': 'Logout',
            'url': 'logout',
            'validators': ['menu_generator.validators.is_authenticated']
        },
        {
            'name': 'Persons',
            'url': 'persons',
            'validators': ['menu_generator.validators.is_authenticated']
        },
        {
            'name': 'Groups',
            'url': 'groups',
            'validators': ['menu_generator.validators.is_authenticated']
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
            ],
        },
    ]
}
