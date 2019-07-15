from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables
#from django_tables2.utils import A


class PersonsTable(tables.Table):
    class Meta:
        attrs = {'class': 'table table-striped table-bordered table-hover table-responsive-xl'}

    first_name = tables.Column(verbose_name=_('First name'))
    last_name = tables.Column(verbose_name=_('Last name'))
