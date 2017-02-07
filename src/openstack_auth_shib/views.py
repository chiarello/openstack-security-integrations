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

from django import shortcuts
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from openstack_auth.views import login as basic_login
from openstack_auth.views import websso as basic_websso
from openstack_auth.views import logout as basic_logout
from openstack_auth.views import switch as basic_switch
from openstack_auth.views import switch_region as basic_switch_region
from openstack_auth.utils import is_websso_enabled

from horizon import forms

from .forms import RegistrForm
from .idpmanager import get_manager

LOG = logging.getLogger(__name__)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request):

    return basic_login(request)


@sensitive_post_parameters()
@csrf_exempt
@never_cache
def websso(request):

    if is_websso_enabled():
        return basic_websso(request)

    tempDict = {
        'error_header' : _("Web SSO error"),
        'error_text' : _("Web SSO is not supported"),
        'redirect_url' : '/dashboard',
        'redirect_label' : _("Home")
    }
    return shortcuts.render(request, 'aai_error.html', tempDict)

def logout(request):

    return basic_logout(request)


@login_required
def switch(request, tenant_id, redirect_field_name=REDIRECT_FIELD_NAME):
    # workaround for switch redirect: don't use the redirect field name
    return basic_switch(request, tenant_id, '')

@login_required
def switch_region(request, region_name, redirect_field_name=REDIRECT_FIELD_NAME):
    # workaround for switch redirect: don't use the redirect field name
    return basic_switch_region(request, region_name, '')

class RegistrView(forms.ModalFormView):
    form_class = RegistrForm
    template_name = 'registration.html'

    def get_initial(self):
        result = super(RegistrView, self).get_initial()
        attributes = get_manager(self.request)

        if attributes:
            result['needpwd'] = False
            result['username'] = attributes.username
            result['federated'] = "true"
            if attributes.givenname:
                result['givenname'] = attributes.givenname
            if attributes.sn:
                result['sn'] = attributes.sn
            if attributes.email:
                result['email'] = attributes.email
            if attributes.provider:
                result['organization'] = attributes.provider
        else:
            result['needpwd'] = True
            result['federated'] = "false"

        return result

    def get_context_data(self, **kwargs):
        context = super(RegistrView, self).get_context_data(**kwargs)
        attributes = get_manager(self.request)
        if attributes:
            context['userid'] = attributes.username
            context['form_action_url'] = '%s/auth/register/' % attributes.root_url
        else:
            context['form_action_url'] = '/dashboard/auth/register/'
        return context

def reg_done(request):
    tempDict = {
        'redirect_url' : '/dashboard',
        'redirect_label' : _("Home")
    }
    return shortcuts.render(request, 'aai_registration_ok.html', tempDict)

def reg_failure(request):
    tempDict = {
        'error_header' : _("Registration error"),
        'error_text' : _("A failure occurs registering user"),
        'contacts' : getattr(settings, 'MANAGERS', None),
        'redirect_url' : '/dashboard',
        'redirect_label' : _("Home")
    }
    return shortcuts.render(request, 'aai_error.html', tempDict)

def name_exists(request):
    tempDict = {
        'error_header' : _("Registration error"),
        'error_text' : _("Login name or project already exists, please, choose another one"),
        'redirect_url' : '/dashboard',
        'redirect_label' : _("Home")
    }
    return shortcuts.render(request, 'aai_error.html', tempDict)

def dup_login(request):
    tempDict = {
        'error_header' : _("Registration error"),
        'error_text' : _("Request has already been sent"),
        'redirect_url' : '/dashboard',
        'redirect_label' : _("Home")
    }
    return shortcuts.render(request, 'aai_error.html', tempDict)

#
# Used in /etc/shibboleth/shibboleth2.xml
#
def auth_error(request):

    if 'errorText' in request.GET:
        err_msg = "%s: [%s]" % (_("Original error"), request.GET['errorText'])
    else:
        err_msg = _("A failure occurs authenticating user")
    
    tempDict = {
        'error_header' : _("Authentication error"),
        'error_text' : err_msg,
        'contacts' : getattr(settings, 'MANAGERS', None),
        'redirect_url' : '/dashboard',
        'redirect_label' : _("Home")
    }
    return shortcuts.render(request, 'aai_error.html', tempDict)













