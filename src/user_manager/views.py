import logging

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from horizon import exceptions

from openstack_dashboard.dashboards.admin.users.views import IndexView as BaseIndexView
from openstack_dashboard.dashboards.admin.users.views import UpdateView as BaseUpdateView
from openstack_dashboard.dashboards.admin.users.views import CreateView as BaseCreateView

from openstack_auth_shib.models import Registration

from openstack_dashboard import api

from .tables import UsersTable

LOG = logging.getLogger(__name__)

class ExtUserItem:
    def __init__(self, usr_data):
        self.id = usr_data.id
        self.name = usr_data.name
        self.enabled = usr_data.enabled
        self.email = usr_data.email
        self.expiration = None
    
    def __cmp__(self, other):
        return cmp(self.name, other.name)

class IndexView(BaseIndexView):
    table_class = UsersTable
    template_name = 'admin/user_manager/index.html'

    def get_data(self):
        usr_table = dict()
        
        #
        # TODO very heavy, need improvements
        #      missing paging
        #
        for item in super(IndexView, self).get_data():
            usr_table[item.id] = ExtUserItem(item)
        
        exp_list = Registration.objects.filter(
            userid__in=usr_table.keys()
        )
        
        for item in exp_list:
            usr_table[item.userid].expiration = item.expdate
        
        result = usr_table.values()
        result.sort()
        return result

class UpdateView(BaseUpdateView):
    template_name = 'admin/user_manager/update.html'
    success_url = reverse_lazy('horizon:admin:user_manager:index')

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = api.keystone.user_get(self.request,
                                                     self.kwargs['user_id'],
                                                     admin=True)
            except Exception:
                redirect = reverse_lazy('horizon:admin:user_manager:index')
                exceptions.handle(self.request, _('Unable to update user.'),
                                  redirect=redirect)
        return self._object

class CreateView(BaseCreateView):
    template_name = 'admin/user_manager/create.html'
    success_url = reverse_lazy('horizon:admin:user_manager:index')

