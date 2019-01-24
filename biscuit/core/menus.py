from django.urls import reverse

from menu import Menu, MenuItem

Menu.add_item('main', MenuItem('Login',
                               reverse('login'),
                               check=lambda request: request.user.is_anonymous))

Menu.add_item('main', MenuItem('Logout',
                               reverse('logout'),
                               check=lambda request: request.user.is_authenticated))
