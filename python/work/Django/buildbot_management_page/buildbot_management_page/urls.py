from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('buildbot_management_page.management_page.views',
    url(r"^$", "index"),
	url(r"^index/$", "index"),
    url(r"^win_dvdfab_build/$", "win_dvdfab_build"),
	url(r"^mac_dvdfab_build/$", "mac_dvdfab_build"),
    url(r"^tdmore_build/$", "tdmore_build"),
    url(r"^safedvdcopy_build/$", "safedvdcopy_build"),
    url(r"^mac_safedvdcopy_build/$", "mac_safedvdcopy_build"),
    url(r"^mac_safedvdcopy_backup_build/$", "mac_safedvdcopy_backup_build"),
    url(r"^win_dvdfab_official_build/$", "win_dvdfab_official_build"),
    url(r"^mac_dvdfab_official_build/$", "mac_dvdfab_official_build"),
	
    url(r"^vidon_xbmc/$", "vidon_xbmc"),
    # Examples:
    # url(r'^$', 'buildbot_management_page.views.home', name='home'),
    # url(r'^buildbot_management_page/', include('buildbot_management_page.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
