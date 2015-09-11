from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('display_files.views',
    url(r'^develop/', 'develop'),        
    # Examples:
    # url(r'^$', 'mydisplay_files.views.home', name='home'),
    # url(r'^mydisplay_files/', include('mydisplay_files.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
