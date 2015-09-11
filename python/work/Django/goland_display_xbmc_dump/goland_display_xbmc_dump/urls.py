from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('goland_display_xbmc_dump.display_xbmc_dump.views',
    url(r"^$", "index"),
    url(r"^index/$", "index"),
    url(r"^download_dump/$", "download_dump"),
    url(r"^display_log_content/(?P<param>\d*)/$", "display_log_content"),
    url(r"^one_record/(?P<param>\d*)/$", "one_record"),
    #url(r"^search_result/$", "search_result"),
    # Examples:
    # url(r'^$', 'goland_display_xbmc_dump.views.home', name='home'),
    # url(r'^goland_display_xbmc_dump/', include('goland_display_xbmc_dump.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
