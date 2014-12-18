#  Copyright (c) 2014 INFN - "Istituto Nazionale di Fisica Nucleare" - Italy
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License. 

import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from horizon import tables

LOG = logging.getLogger(__name__)

class DeleteProviderAction(tables.DeleteAction):
    data_type_singular = _("Provider")
    data_type_plural = _("Providers")

    #
    # TODO to be implemented
    #
    def delete(self, request, obj_id):
        pass
        #with transaction.commit_on_success():


class AddProviderAction(tables.LinkAction):
    name = "add_provider"
    verbose_name = _("Add Provider")
    url = "horizon:project:idp_requests:manage"
    classes = ("btn-launch", "ajax-modal",)


class IdPTable(tables.DataTable):
    idpid = tables.Column('idpid', verbose_name=_('Provider ID'))
    username = tables.Column('username', verbose_name=_('User name'))

    class Meta:
        name = "idp_table"
        verbose_name = _("Providers")
        row_actions = (DeleteProviderAction, )
        table_actions = (AddProviderAction, DeleteProviderAction, )

    def get_object_id(self, datum):
        return datum.idpid

