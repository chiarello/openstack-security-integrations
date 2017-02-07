#HORIZON_CONFIG['user_home'] = 'openstack_auth_shib.utils.get_user_home'

AUTHENTICATION_URLS = ['openstack_auth_shib.urls']

INSTALLED_APPS.append('openstack_auth_shib')

NOTIFICATION_TEMPLATE_DIR = '/etc/openstack-auth-shib/notifications'

#DATABASES = {
#    'default': {
#        'ENGINE' : 'django.db.backends.mysql',
#        'NAME' : '',
#        'USER' : '',
#        'PASSWORD' : '',
#        'HOST' : '',
#        'PORT' : '3306'
#    }
#}

