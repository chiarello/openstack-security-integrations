from django.utils.translation import ugettext_lazy as _

from horizon import exceptions

from openstack_dashboard.dashboards.admin.projects.views import IndexView as BaseIndexView
from openstack_dashboard.dashboards.admin.projects.views import CreateProjectView
from openstack_dashboard.dashboards.admin.projects.views import UpdateProjectView as BaseUpdateProjectView
from openstack_dashboard.dashboards.admin.projects.views import ProjectUsageView
from openstack_dashboard import api

from .tables import ProjectsTable
from .workflows import UpdateProject

from openstack_auth_shib.models import Project

class ExtPrjItem:
    def __init__(self, prj_data):
        self.id = prj_data.id
        self.name = prj_data.name
        self.description = prj_data.description
        self.enabled = prj_data.enabled
        self.visible = False

class IndexView(BaseIndexView):
    table_class = ProjectsTable
    template_name = 'admin/projects/index.html'

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        result = list()
        marker = self.request.GET.get(ProjectsTable._meta.pagination_param, None)
        domain_context = self.request.session.get('domain_context', None)
        try:
            tenants, self._more = api.keystone.tenant_list(
                self.request, domain=domain_context,
                paginate=True, marker=marker)
            
            prj_table = dict()
            for item in tenants:
                prj_table[item.name] = ExtPrjItem(item)
            
            prj_list = Project.objects.filter(projectname__in=prj_table.keys())
            for prj_item in prj_list:
                prj_table[prj_item.projectname].visible = prj_item.visible
            
            tmplist = prj_table.keys()
            tmplist.sort()
            for item in tmplist:
                result.append(prj_table[item])
            
        except Exception:
            self._more = False
            exceptions.handle(self.request, _("Unable to retrieve project list."))
        return result


class UpdateProjectView(BaseUpdateProjectView):
    workflow_class = UpdateProject

