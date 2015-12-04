from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('create_build.views',
    url(r"^register/$","register"),
    url(r"^login/$","login"),
    url(r"^logout/$","logout"),
    url(r"^$","index"),
    url(r"^index/$","index"),
    url(r"^create_new_build/$","create_new_build"),
    url(r"^display_all_records/$","display_all_records"),
    url(r"^display_all_used_records/$","display_all_used_records"),
    url(r"^search_info/$","search_info"),
    url(r"^empty/$","empty"),
    url(r"^update_info_page/(?P<params>\d*)/$","update_info_page"),
    url(r"^update_info/(?P<params>\d*)/$","update_info"),
    url(r"^display_details/(?P<params>\d*)/$","display_details"),
    url(r"^delete/(?P<params>\d*)/$","delete"),
    url(r"^get_passwd_page/$","get_passwd_page"),
    url(r"^get_passwd/$","get_passwd"),
    url(r"^checkname/$","checkname"),
    # Examples:
    # url(r'^$', 'auto_create_build.views.home', name='home'),
    # url(r'^auto_create_build/', include('auto_create_build.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
