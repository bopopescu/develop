from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('DVDFab_Information.DVDFab.views',
    url(r"^$", "index"),
    url(r"^index/$", "index"),
    url(r"^ci_file/$", "ci_file"),
    url(r"^add_branch/$", "add_branch"),
    url(r"^modify_branch/$", "modify_branch"),
    url(r"^modify_compile/$", "modify_compile"),
    url(r"^add_name/$", "add_name"),
    url(r"^search_info/$", "search_info"),
    url(r"^modify_change_log/$", "modify_change_log"),
    url(r"^update_change_log/$", "update_change_log"),
    # Examples:
    # url(r'^$', 'DVDFab_Information.views.home', name='home'),
    # url(r'^DVDFab_Information/', include('DVDFab_Information.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('DVDFab_Information.Backup_DVDFab.views',
    url(r"^main/$", "main"),
    url(r"^display_information/$", "display_information"),
    url(r"^backup_dvdfab/$", "backup_dvdfab"),
    url(r"^backup_result/$", "backup_result"),
    url(r"^display_all/$", "display_all"),
    url(r"^display_all_record/$", "display_all_record"),
    url(r"^display_all_information/(?P<param>\d*)$", "display_all_information"),
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('DVDFab_Information.Backup_VDMServer.views',
    url(r"^main/$", "main"),
    url(r"^display_vdmserver_information/$", "display_vdmserver_information"),
    url(r"^backup_vdmserver/$", "backup_vdmserver"),
    url(r"^backup_result/$", "backup_result"),
    url(r"^display_all_vdmserver/$", "display_all_vdmserver"),
    url(r"^display_all_vdmserver_record/$", "display_all_vdmserver_record"),
    url(r"^display_all_vdmserver_information/(?P<param>\d*)$", "display_all_vdmserver_information"),
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('DVDFab_Information.Backup_TDMore.views',
    url(r"^main/$", "main"),
    url(r"^display_tdmore_information/$", "display_tdmore_information"),
    url(r"^backup_tdmore/$", "backup_tdmore"),
    url(r"^backup_result/$", "backup_result"),
    url(r"^display_all_tdmore/$", "display_all_tdmore"),
    url(r"^display_all_tdmore_record/$", "display_all_tdmore_record"),
    url(r"^display_all_tdmore_information/(?P<param>\d*)$", "display_all_tdmore_information"),
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('DVDFab_Information.Backup_VidOnme.views',
    url(r"^main/$", "main"),
    url(r"^display_vidonme_information/$", "display_vidonme_information"),
    url(r"^backup_vidonme/$", "backup_vidonme"),
    url(r"^backup_result/$", "backup_result"),
    url(r"^display_all_vidonme/$", "display_all_vidonme"),
    url(r"^display_all_vidonme_record/$", "display_all_vidonme_record"),
    url(r"^display_all_vidonme_information/(?P<param>\d*)$", "display_all_vidonme_information"),
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('DVDFab_Information.Backup_SafeDVDCopy.views',
    url(r"^main/$", "main"),
    url(r"^display_safedvdcopy_information/$", "display_safedvdcopy_information"),
    url(r"^backup_safedvdcopy/$", "backup_safedvdcopy"),
    url(r"^backup_result/$", "backup_result"),
    url(r"^display_all_safedvdcopy/$", "display_all_safedvdcopy"),
    url(r"^display_all_safedvdcopy_record/$", "display_all_safedvdcopy_record"),
    url(r"^display_all_safedvdcopy_information/(?P<param>\d*)$", "display_all_safedvdcopy_information"),
    #url(r'^admin/', include(admin.site.urls)),
)
