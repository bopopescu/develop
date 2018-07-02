#在settings文件里配置LDAP，其他相关配置都已去掉，只保留了LDAP的配置


    
import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
from django.conf.global_settings import AUTHENTICATION_BACKENDS


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

