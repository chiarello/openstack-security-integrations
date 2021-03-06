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

try:
    from django.conf.urls import patterns, url
except:
    from django.conf.urls.defaults import patterns, url

from openstack_dashboard.dashboards.idmanager.registration_manager import views

prefix = 'openstack_dashboard.dashboards.idmanager.registration_manager.views'

urlpatterns = patterns(prefix,
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^(?P<requestid>[^/]+)/precheck/$', views.PreCheckView.as_view(), name='precheck'),
    url(r'^(?P<requestid>[^/]+)/grantall/$', views.GrantAllView.as_view(), name='grantall'),
    url(r'^(?P<requestid>[^/]+)/reject/$', views.RejectView.as_view(), name='reject'),
    url(r'^(?P<requestid>[^/]+)/forcedapprove/$', views.ForcedApproveView.as_view(), 
        name='forcedapprove'),
    url(r'^(?P<requestid>[^/]+)/forcedreject/$', views.ForcedRejectView.as_view(), 
        name='forcedreject'),
    url(r'^(?P<requestid>[^/]+)/newproject/$', views.NewProjectView.as_view(), 
        name='newproject'),
    url(r'^(?P<requestid>[^/]+)/rejectproject/$', views.RejectProjectView.as_view(), 
        name='rejectproject'),
    url(r'^(?P<requestid>[^/]+)/guestapprove/$', views.GuestApproveView.as_view(), 
        name='guestapprove'),
    url(r'^(?P<requestid>[^/]+)/renewadmin/$', views.RenewAdminView.as_view(), 
        name='renewadmin')
    )

