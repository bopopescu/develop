from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('goland_developer_manage_platform.developer_manage_platform.views',
    url(r"^$", "index"),
	url(r"^index/$", "index"),
	#BluFab
    #url(r"^dvdfab_developer_daily_build/$", "dvdfab_developer_daily_build"),
	url(r"^blufab_daily_build/$", "blufab_daily_build"),
	url(r"^blufab_release_package/$", "blufab_release_package"),
    #url(r"^blufab_official_package/$", "blufab_official_package"),
	url(r"^blufab_crash_dump/$", "blufab_crash_dump"),
    #url(r"^mac_dvdfab_developer_daily_build/$", "mac_dvdfab_developer_daily_build"),
	url(r"^mac_blufab_daily_build/$", "mac_blufab_daily_build"),
	url(r"^mac_blufab_release_package/$", "mac_blufab_release_package"),
    #url(r"^mac_dvdfab_official_package/$", "mac_dvdfab_official_package"),
	
    #DVDFab
    url(r"^dvdfab_developer_daily_build/$", "dvdfab_developer_daily_build"),
	url(r"^dvdfab_daily_build/$", "dvdfab_daily_build"),
	url(r"^dvdfab_release_package/$", "dvdfab_release_package"),
    url(r"^safedvdcopy/$", "safedvdcopy"),
    url(r"^dvdfab_official_package/$", "dvdfab_official_package"),
	url(r"^dvdfab_crash_dump/$", "dvdfab_crash_dump"),
    url(r"^mac_dvdfab_developer_daily_build/$", "mac_dvdfab_developer_daily_build"),
	url(r"^mac_dvdfab_daily_build/$", "mac_dvdfab_daily_build"),
	url(r"^mac_dvdfab_release_package/$", "mac_dvdfab_release_package"),
    url(r"^mac_dvdfab_official_package/$", "mac_dvdfab_official_package"),
	
	#DVDFab Media Player2
	url(r"^player_release_package/$", "player_release_package"),
	url(r"^player_crash_dump/$", "player_crash_dump"),
	url(r"^mac_player_daily_build/$", "mac_player_daily_build"),
	url(r"^mac_player_release_package/$", "mac_player_release_package"),
	
	#VidOn Server
	url(r"^vidon_server_daily_build/$", "vidon_server_daily_build"),
	url(r"^vidon_server_release_package/$", "vidon_server_release_package"),
	url(r"^vidon_server_crash_dump/$", "vidon_server_crash_dump"),
	
	#VidOn XBMC
        url(r"^linux_vbox1_package/$", "linux_vbox1_package"),             
	url(r"^vidon_xbmc_daily_build/$", "vidon_xbmc_daily_build"),
	url(r"^linux_vidon_xbmc_av500_daily_build/$", "linux_vidon_xbmc_av500_daily_build"),
	url(r"^linux_vidon_xbmc_daily_build/$", "linux_vidon_xbmc_daily_build"),
	url(r"^linux_vidon_xbmc_release_package/$", "linux_vidon_xbmc_release_package"),
	url(r"^linux_vidon_xbmc_crash_dump/$", "linux_vidon_xbmc_crash_dump"),
	
	#VidOn.Me Mobile
	url(r"^vidonmemobile_android/$", "vidonmemobile_android"),
	url(r"^vidonmemobile_ios/$", "vidonmemobile_ios"),
    # Examples:
    # url(r'^$', 'goland_developer_manage_platform.views.home', name='home'),
    # url(r'^goland_developer_manage_platform/', include('goland_developer_manage_platform.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
