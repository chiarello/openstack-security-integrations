import logging

from django.utils.translation import ugettext_lazy as _

from openstack_auth_shib.models import RegRequest

from horizon import tables

LOG = logging.getLogger(__name__)

class ApproveLink(tables.LinkAction):
    name = "approve"
    verbose_name = _("Approve")
    url = "horizon:admin:registration_manager:approve"
    classes = ("ajax-modal", "btn-edit")

class DiscardAction(tables.DeleteAction):
    data_type_singular = _("Registration")
    data_type_plural = _("Registrations")

    def delete(self, request, obj_id):
        LOG.debug("Discarding registration for %s" % obj_id)
        RegRequest.objects.filter(uname=obj_id).delete()
        #
        # TODO send notification via mail
        #


class RegisterTable(tables.DataTable):
    reqid = tables.Column('reqid', verbose_name=_('Request ID'))
    localuser = tables.Column('localuser', verbose_name=_('Cloud User'))
    email = tables.Column('email', verbose_name=_('Email address'))
    notes = tables.Column('notes', verbose_name=_('Notes'))
    globalid = tables.Column('globalid', verbose_name=_('Global user ID'))
    idp = tables.Column('idp', verbose_name=_('Identity Provider'))
    domain = tables.Column('domain', verbose_name=_('Domain'))

    class Meta:
        name = "register_table"
        verbose_name = _("Registrations")
        row_actions = (ApproveLink, DiscardAction,)
        table_actions = (DiscardAction,)

    def get_object_id(self, datum):
        return datum.reqid
