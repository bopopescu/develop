from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('DVDFabMediaPlayer_analysis_report.analysis_report.views',
    url(r"^$", "index"),
    url(r"^index/$", "index"),
    url(r"^(?P<param1>\d*)/$", "display_each_day"),
    url(r"^(?P<param1>\d*)/(?P<param2>\w*)/$", "display_details"),
    # Examples:
    # url(r'^$', 'DVDFabMediaPlayer_analysis_report.views.home', name='home'),
    # url(r'^DVDFabMediaPlayer_analysis_report/', include('DVDFabMediaPlayer_analysis_report.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
