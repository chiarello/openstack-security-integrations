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

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import horizon

from openstack_dashboard.dashboards.idmanager import dashboard

def enableIdPRequests(obj, context):
    request = context['request']
    if 'INFN-testing' in request.META.get('HTTP_USER_AGENT',''):
        return True
    return False

class IdPRequests(horizon.Panel):
    name = _("Identity Providers")
    slug = 'idp_requests'
    nav = enableIdPRequests

dashboard.IdentityManager.register(IdPRequests)

