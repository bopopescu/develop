from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('publish.views',
    url(r"^$", "index", name = "index"),
    url(r"^index/$", "index", name = "index"),
    url(r"^add_product/$", "add_product", name = "add_product_name"),
    url(r"^add_product_management/$", "add_product_management", name = "add_product_management_name"),
    url(r"^search_product_management/$", "search_product_management", name = "search_product_management"),
    url(r"^publish_revert/(?P<params>\d+)/$", "publish_revert", name = "publish_revert"),
    url(r"^show_product/$", "show_product", name = "show_product"),
    url(r"^update_product/(?P<params>\d+)/$", "update_product", name = "update_product"),
    url(r"^delete_product/(?P<params>\d+)/$", "delete_product", name = "delete_product"),
    url(r"^delete_product_management/$", "delete_product_management", name = "delete_product_management"),
    url(r"^show_history/$", "show_history", name = "show_history"),
    url(r"^login/$", "login", name = "login_name"),
    url(r"^logout/$", "logout", name = "logout"),
    #url(r"^test/$", "test_view", name = "test_name"),
    url(r"^forbidden/$", "forbidden", name = "forbidden_name"),

    url(r"^api/v1/update/pre_imagename/$", "update_pre_imagename", name = "update_pre_imagename"),
    url(r"^api/v1/update/main_imagename/$", "update_main_imagename", name = "update_main_imagename"),
    url(r"^api/v1/update/pub_flag/$", "update_pub_flag", name = "update_pub_flag"),
    url(r"^api/v1/get/main_imagename/$", "get_main_imagename", name = "get_main_imagename"),
    #url(r'^publish/', include('publish.urls')),
    # Examples:
    # url(r'^$', 'code_publish.views.home', name='home'),
    # url(r'^code_publish/', include('code_publish.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
