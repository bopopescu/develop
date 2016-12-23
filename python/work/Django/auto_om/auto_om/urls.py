from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os

from om import models
#import settings

search_list = ["platform", "ip", "username", "is_virtual"]
record_list = ["platform", "ip", "memory", "cpu", "hard_disk", "username", "password", "is_virtual", "join_date", "modify_date", "status", "description"]

staff_search_list = ["platform", "department", "staff_name", "ip"]
staff_record_list = ["platform", "department", "staff_name", "ip", "asset_name", "serial_num", "asset_address", "memory", "cpu", "hard_disk", "status", "description"]


urlpatterns = patterns('om.views',
    #url(r'^static/(?P<name>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(os.path.realpath(admin.__file__)), 'static')}),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r"^test/$", "test"),
    url(r"^test1/$", "test1"),
    url(r"^test2/$", "test2"),
    url(r"^test3/$", "test3"),
    url(r"^test4/$", "test4"),
    url(r"^$", "index", {"template": "index.html", "model": models.PC_Info, "search_list": search_list, "record_list": record_list, "total_pc_flag": True}),
    url(r"^login/$", "login"),
    url(r"^accounts/login/$", "login"),
    url(r"^logout/$", "logout"),
    url(r"^accounts/logout/$", "logout"),
    url(r"^index/$", "index"),
    url(r"^add_pc/$", "add_pc"),
    url(r"^update/$", "update"),
    url(r"^update/(?P<params>\d+)/$", "update"),
    #url(r"^update/(\d+)/$", "update"),
    url(r"^delete/$", "delete"),
    url(r"^delete/(?P<params>\d+)/$", "delete", {"model": models.PC_Info, "url": "/"}),
    #url(r"^shutdown/(?P<params>\d+)/$", "shutdown"),
    url(r"^shutdown_all/$", "shutdown_all"),
    url(r"^display_operation_record/$", "display_operation_record"),
    url(r"^display_esxi/$", "display_esxi"),
    
    url(r"^create_virtual/$", "create_virtual"),
    url(r"^add_ip/$", "add_ip"),
    url(r"^display_ip_list/$", "display_ip_list"),
    url(r"^update_ip/(?P<params>\d+)/$", "update_ip"),
    url(r"^delete_ip/(?P<params>\d+)/$", "delete_ip", {"model": models.IP, "url": "/display_ip_list"}),
   
    url(r"^display_staff_info/$", "display_staff_info", {"template": "display_staff_info.html", "model": models.Staff_Info, "search_list": staff_search_list, "record_list": staff_record_list, "total_pc_flag": False}),
    url(r"^add_staff_info/$", "add_staff_info"),
    url(r"^update_staff_info/(?P<params>\d+)/$", "update_staff_info"),
    url(r"^delete_staff_info/(?P<params>\d+)/$", "delete_staff_info", {"model": models.Staff_Info, "url": "/display_staff_info"}),
    url(r"^display_user_permission/$", "display_user_permission"),
    
    url(r"^export_excel/$", "export_excel"),
    url(r"^export_server_info_to_excel/$", "export_server_info_to_excel"),

    # Examples:
    # url(r'^$', 'auto_om.views.home', name='home'),
    # url(r'^auto_om/', include('auto_om.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


