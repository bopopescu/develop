# Django settings for auto_create_build project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
from django.conf.global_settings import AUTHENTICATION_BACKENDS

import os
BASE_DIR = os.path.dirname(__file__)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
XDD = "haha"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'auto_create_build',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'sjgldb',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace("\\","/")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8glus=e-@*cn$$-*9=w_fzki4@^a@9sdq30@u1-5i2yx5j9umc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	#'D:/develop/auto_create_build/templates/html',
        os.path.join(BASE_DIR, "templates").replace("\\","/"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'create_build',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}





LOGGING = {  
    'version': 1,  
    'disable_existing_loggers': True,  
    'formatters': {  
        'standard': {  
  
            #'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'  
			'format': '%(asctime)s [%(levelname)s]- %(message)s'  
        },  
    },  
    'filters': {  
    },  
    'handlers': {  
        'mail_admins': {  
            'level': 'ERROR',  
            'class': 'django.utils.log.AdminEmailHandler',  
            'include_html': True,  
        },  
        'default': {  
            'level':'DEBUG',  
            'class':'logging.handlers.RotatingFileHandler',  
            'filename': "/home/goland/log.txt", 
            'maxBytes': 1024*1024*500, # 500 MB  
            'backupCount': 5,  
            'formatter':'standard',  
        },   
    },  
    'loggers': {  
        'django': {  
            'handlers': ['default'],  
            'level': 'INFO',  
            'propagate': False  
        },  
       
    }  
} 


###################below is the LDAP configration#############################
AUTH_LDAP_SERVER_URI = "ldap://10.10.7.120:389"

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS:  0,
}

ad_name = 'CN=徐德东,OU=IT部,OU=世纪高蓝,DC=goland,DC=cn'.decode("utf-8")
search_ad = 'OU=世纪高蓝,DC=goland,DC=cn'.decode("utf-8")
AUTH_LDAP_BIND_DN = ad_name
AUTH_LDAP_BIND_PASSWORD = "123456"

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch(search_ad, ldap.SCOPE_SUBTREE, "(&(objectClass=user)(mail=%(user)s))"),
    LDAPSearch(search_ad, ldap.SCOPE_SUBTREE, "(&(objectClass=user)(sAMAccountName=%(user)s))"),
)



AUTH_LDAP_USER_ATTR_MAP = {
'first_name':'givenName',
'last_name':'sn',
'email':'mail',
}


AUTHENTICATION_BACKENDS = (
'django_auth_ldap.backend.LDAPBackend',
'django.contrib.auth.backends.ModelBackend',
) 

AUTH_LDAP_ALWAYS_UPDATE_USER = True
#AUTH_LDAP_FIND_GROUP_PERMS = True

AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: False,
    ldap.OPT_REFERRALS: False,
}

