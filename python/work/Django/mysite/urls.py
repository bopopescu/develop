from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blog.views',
    url(r'^upload/$','upload'),
    url(r'^$','index'),
    url(r'^index/$','index'),
    url(r'^new_add_case/$','new_add_case'),
    url(r'^new_add_client/$','new_add_client'),
    url(r'^new_add_BD/$','new_add_BD'),
    url(r'^new_add_DVD/$','new_add_DVD'),
    url(r'^new_add_BD3D/$','new_add_BD3D'),
    url(r'^new_add_version/$','new_add_version'),

    url(r'^case/$','case'),
    url(r'^insert_session/$','insert_session'),
    url(r'^client/$','client'),
    url(r'^version/$','version'),
    url(r'^bd_samples/$','bd_samples'),
    url(r'^dvd_samples/$','dvd_samples'),
    url(r'^bd3d_samples/$','bd3d_samples'),
    url(r'^all_samples/$','all_samples'),
    url(r'^session/$','session'),
    url(r'^search/DVD/$','search_DVD'),
    url(r'^search/BD/$','search_BD'),
    url(r'^search/3D/$','search_3D'),
    url(r'^search/File/$','search_File'),
    url(r'^test_result/$','test_result'),
    url(r'^search_type/$','search_type'),

    url(r'^search/BD/type/$','search_BD_type'),
    url(r'^search/DVD/type/$','search_DVD_type'),
    url(r'^search/BD3D/type/$','search_BD3D_type'),
    url(r'^search/all/type/$','search_all_type'),
    url(r'^search/session/$','search_session'),
    url(r'^search_test_result/$','search_test_result'),


    url(r'^BD/sort/$','BD_sort'),
    url(r'^DVD/sort/$','DVD_sort'),
    url(r'^BD3D/sort/$','BD3D_sort'),

    url(r'^update_case_page/(?P<param1>\d*)/$','update_case_page'),
    url(r'^update_case/(?P<param1>\d*)/$','update_case'),

    #url(r'^update_client_page/(?P<param1>\d*)/$','update_client_page'),
    #url(r'^update_client/(?P<param1>\d*)/$','update_client'),
    url(r'^update_client_page$','update_client_page'),
    url(r'^update_client/(?P<param1>\d*)/$','update_client'),

    url(r'^update_version_page/(?P<param1>\d*)/$','update_version_page'),
    url(r'^update_version/(?P<param1>\d*)/$','update_version'),

    url(r'^update_BD_page/(?P<param1>\d*)/$','update_BD_page'),

    url(r'^update_BD/(?P<param1>\d*)/$','update_BD'),

    url(r'^update_DVD_page/(?P<param1>\d*)/$','update_DVD_page'),
    url(r'^update_DVD/(?P<param1>\d*)/$','update_DVD'),

    url(r'^update_BD3D_page/(?P<param1>\d*)/$','update_BD3D_page'),
    url(r'^update_BD3D/(?P<param1>\d*)/$','update_BD3D'),

    #url(r'^update_all_page/(?P<param1>\d*)/$','update_all_page'),
    url(r'^update_all_BD_page/(?P<param1>\d*)/$','update_all_BD_page'),
    url(r'^update_all_DVD_page/(?P<param1>\d*)/$','update_all_DVD_page'),
    url(r'^update_all_BD3D_page/(?P<param1>\d*)/$','update_all_BD3D_page'),
    url(r'^update_all_BD/(?P<param1>\d*)/$','update_all_BD'),
    url(r'^update_all_DVD/(?P<param1>\d*)/$','update_all_DVD'),
    url(r'^update_all_BD3D/(?P<param1>\d*)/$','update_all_BD3D'),
    #url(r'^update_all/(?P<param1>\d*)/$','update_all'),


    url(r'^update_session_page/(?P<param1>\d*)/$','update_session_page'),
    url(r'^update_session/(?P<param1>\d*)/$','update_session'),

    url(r'^update_test_result_page/(?P<param1>\d*)/$','update_test_result_page'),
    url(r'^update_test_result/(?P<param1>\d*)/$','update_test_result'),
    #url(r'^display/days/result/$','display_days_result'),

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
