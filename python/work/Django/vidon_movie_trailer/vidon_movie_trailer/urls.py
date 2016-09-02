from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('movie_trailer.views',
    url(r"^$","index"),
    url(r"^index/$","index"),
    #url(r"^copy_build/(?P<params>\d*)/$","copy_build"),
    url(r"^display_movie_info/(?P<params>\d*)/$","display_movie_info"),
    url(r"^download_movie/$","download_movie"),
    # Examples:
    # url(r'^$', 'vidon_movie_trailer.views.home', name='home'),
    # url(r'^vidon_movie_trailer/', include('vidon_movie_trailer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
