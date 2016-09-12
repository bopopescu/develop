from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from blog import models
admin.autodiscover()

def get_bd():
    return models.Samples.objects.all()

bd_info = {
             "queryset": models.Samples.objects.all(), 
             "template_name": "BD.html",
             "template_object_name": "samples",
             "extra_context":{"obj_list": get_bd}}

def get_version():
    return models.Versions.objects.all()

version_info = {
             "queryset": models.Versions.objects.all(), 
             "template_name": "version.html",
             #"template": "version.html",
             "template_object_name": "version",
             "extra_context":{"obj_list": get_version}}


urlpatterns = patterns('blog.views',
    url(r'^bd_test/$', list_detail.object_list, bd_info),
    url(r'^version_test/$', direct_to_template, {"template": "version.html", "extra_context":{"obj_list": get_version}}),
    url(r'^version_test1/$', list_detail.object_list, version_info),
    #url(r'^about/$', "about", {"template":"about.html", "extra_context": {"xdd":"123213"}}),
    url(r'^about/$', direct_to_template, {"template":"about.html", "extra_context": {"xdd":"123213"}}),
    url(r'^version/$','object_list', {"template_name": "version.html", "model": models.Versions}),
    url(r'^BD/$','object_list', {"template_name": "BD.html", "model": models.Samples}),
    url(r'^DVD/$','object_list', {"template_name": "DVD.html", "model": models.DVD_samples}),
    url(r'^BD3D/$','object_list', {"template_name": "BD3D.html", "model": models.BD3D_samples}),
    url(r'^test_url/(?P<year>\d{4})/$','test_url', {"template_name": "4040.html"}),
    url(r'^xdd/$','xdd'),
    url(r'^upload/$','upload'),
    url(r'^$','index'),
    url(r'^index/$','index'),
    url(r'^new_add_case/$','new_add_case'),
    url(r'^new_add_client/$','new_add_client'),

    url(r'^new_add_BD/$','new_add_obj', {"template_name": "new_BD.html", "model": models.Samples, "url": "/BD/", "numbers_jar_flag": True}),
    url(r'^new_add_DVD/$','new_add_obj', {"template_name": "new_DVD.html", "model": models.DVD_samples, "url": "/DVD/", "numbers_jar_flag": False}),
    url(r'^new_add_BD3D/$','new_add_obj', {"template_name": "new_BD3D.html", "model": models.BD3D_samples, "url": "/BD3D/", "numbers_jar_flag": True}),
    url(r'^new_add_version/$','new_add_version'),

    url(r'^case/$','case'),
    url(r'^insert_session/$','insert_session'),
    url(r'^client/$','client'),
    url(r'^all_samples/$','all_samples'),
    url(r'^session/$','session'),
    url(r'^search/DVD/$','search_object', {"template_name": "search_DVD.html", "model": models.DVD_samples}),
    url(r'^search/BD/$','search_object', {"template_name": "search_BD.html", "model": models.Samples}),
    url(r'^search/3D/$','search_object', {"template_name": "search_BD3D.html", "model": models.BD3D_samples}),
    url(r'^search/File/$','search_object', {"template_name": "search_File.html", "model": models.BD3D_samples}),
    url(r'^test_result/$','test_result'),
    url(r'^search_type/$','search_type'),
    url(r'^search/BD/type/$','search_object_type', {"template_name": "BD.html", "model": models.Samples, "url": "/BD/"}),
    url(r'^search/DVD/type/$','search_object_type', {"template_name": "DVD.html", "model": models.DVD_samples, "url": "/DVD/"}),
    url(r'^search/BD3D/type/$','search_object_type', {"template_name": "BD3D.html", "model": models.BD3D_samples, "url": "/BD3D/"}),
    url(r'^search/all/type/$','search_all_type'),
    url(r'^search/session/$','search_session'),
    url(r'^search_test_result/$','search_test_result'),

    url(r'^BD/sort/$','object_sort', {"template_name": "BD.html", "model": models.Samples}),
    url(r'^DVD/sort/$','object_sort', {"template_name": "DVD.html", "model": models.DVD_samples}),
    url(r'^BD3D/sort/$','object_sort', {"template_name": "BD3D.html", "model": models.BD3D_samples}),
    url(r'^update_case_page/(?P<param1>\d*)/$','update_case_page'),
    url(r'^update_case/(?P<param1>\d*)/$','update_case'),
    url(r'^update_client/(?P<param1>\d*)/$','update_client'),
    url(r'^update_version/(?P<param1>\d*)/$','update_version'),

    #url(r'^update_BD_page/(?P<param1>\d*)/$','update_BD_page'),
    #url(r'^update_BD/(?P<param1>\d*)/$','update_BD'),
    #url(r'^update_DVD_page/(?P<param1>\d*)/$','update_DVD_page'),
    #url(r'^update_DVD/(?P<param1>\d*)/$','update_DVD'),
    #url(r'^update_BD3D_page/(?P<param1>\d*)/$','update_BD3D_page'),
    #url(r'^update_BD3D/(?P<param1>\d*)/$','update_BD3D'),
    url(r'^update_BD3D/(?P<param1>\d*)/$','update_obj', {"template_name": "update_BD3D.html", "model": models.BD3D_samples, "url": "/BD3D/", "numbers_jar_flag": True}),
    url(r'^update_BD/(?P<param1>\d*)/$','update_obj', {"template_name": "update_BD.html", "model": models.Samples, "url": "/BD/", "numbers_jar_flag": True}),
    url(r'^update_DVD/(?P<param1>\d*)/$','update_obj', {"template_name": "update_DVD.html", "model": models.DVD_samples, "url": "/DVD/", "numbers_jar_flag": False}),
    url(r'^update_all_BD/(?P<param1>\d*)/$','update_obj', {"template_name": "update_all_BD.html", "model": models.Samples, "url": "all_samples", "number_jar_flag": True}),
    url(r'^update_all_DVD/(?P<param1>\d*)/$','update_obj', {"template_name": "update_all_DVD.html", "model": models.DVD_samples, "url": "all_samples", "number_jar_flag": False}),
    url(r'^update_all_BD3D/(?P<param1>\d*)/$','update_obj', {"template_name": "update_all_BD3D.html", "model": models.BD3D_samples, "url": "all_samples", "number_jar_flag": True}),

    #url(r'^update_all_page/(?P<param1>\d*)/$','update_all_page'),
    #url(r'^update_all_BD_page/(?P<param1>\d*)/$','update_all_BD_page'),
    #url(r'^update_all_DVD_page/(?P<param1>\d*)/$','update_all_DVD_page'),
    #url(r'^update_all_BD3D_page/(?P<param1>\d*)/$','update_all_BD3D_page'),
    #url(r'^update_all_BD/(?P<param1>\d*)/$','update_all_BD'),
    #url(r'^update_all_DVD/(?P<param1>\d*)/$','update_all_DVD'),
    #url(r'^update_all_BD3D/(?P<param1>\d*)/$','update_all_BD3D'),
    #url(r'^update_all/(?P<param1>\d*)/$','update_all'),

    url(r'^update_session_page/(?P<param1>\d*)/$','update_session_page'),
    url(r'^update_session/(?P<param1>\d*)/$','update_session', {"url": "/session/"}),
    url(r'^update_test_result_page/(?P<param1>\d*)/$','update_test_result_page'),
    url(r'^update_test_result/(?P<param1>\d*)/$','update_session', {"url": "/test_result/"}),
    url(r'^download_log_folder/(?P<param1>\d*)/$','download_log_folder'),
    url(r'^display_bdverify_log/$','display_bdverify_log'),
    url(r'^display_log/(?P<param1>\d*)/$','display_log'),
    url(r'^upload_file/(?P<param1>\d*)/$', 'upload_file'),
    #url(r'download(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'index', 'show_indexes':True}), 
    url(r'^download/$','download_test_zipfile'),
    url(r'^download_mac/$','download_test_zipfile_for_mac'),
    url(r'^register/$','register'),
    url(r'^login/$','login',{"template_name":"templates/login.html"}, name = "login"),
    #url(r'^accounts/login/$','login',name = "login"),
    url(r'^logout/$','logout'),
    url(r'^test/$','test'),
    url(r'^fenye/$','fenye'),
    url(r'^get_check_code_image/$','get_check_code_image'),


    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
