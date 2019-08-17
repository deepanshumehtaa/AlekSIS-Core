from django.urls import reverse
from django.utils.translation import gettext as _

from menu import Menu, MenuItem

Menu.add_item('main', MenuItem('Login',
                               reverse('login'),
                               check=lambda request: request.user.is_anonymous))

Menu.add_item('main', MenuItem('Logout',
                               reverse('logout'),
                               check=lambda request: request.user.is_authenticated))

Menu.add_item('main', MenuItem(_('Persons'),
                               reverse('persons'),
                               check=lambda request: request.user.is_authenticated))

Menu.add_item('main', MenuItem(_('Groups'),
                               reverse('groups'),
                               check=lambda request: request.user.is_authenticated))
