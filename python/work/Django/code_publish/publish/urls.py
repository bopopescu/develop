from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('publish.views',
    url(r"^$", "index", name = "index"),
    url(r"^index/$", "index", name = "index"),
    url(r"^add_product_management/$", "add_product_management", name = "add_product_management_name"),
    url(r"^search_product_management/$", "search_product_management", name = "search_product_management_name"),
    url(r"^publish/(?P<params>\d+)/$", "publish", name = "publish"),
    url(r"^revert/(?P<params>\d+)/$", "revert", name = "revert"),
    url(r"^show_history/$", "show_history", name = "show_history"),
    url(r"^login/$", "login", name = "login"),
    url(r"^logout/$", "logout", name = "logout"),
    # Examples:
    # url(r'^$', 'code_publish.views.home', name='home'),
    # url(r'^code_publish/', include('code_publish.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
