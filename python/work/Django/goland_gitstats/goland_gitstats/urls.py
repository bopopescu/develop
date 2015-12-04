from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gitstats.views',
    url(r"^$", "index"),
    url(r"^index/$", "index"),
    url(r"^display_author/$", "display_author"),
    url(r"^display_project/$", "display_project"),
    url(r"^display_product_project/$", "display_product_project"),
    url(r"^add_product_project/$", "add_product_project"),
    url(r"^update_product_project/(?P<param>\d*)$", "update_product_project"),
    # Examples:
    # url(r'^$', 'goland_gitstats.views.home', name='home'),
    # url(r'^goland_gitstats/', include('goland_gitstats.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
