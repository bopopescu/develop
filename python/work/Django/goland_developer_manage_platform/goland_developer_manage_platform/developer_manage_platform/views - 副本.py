# Create your views here.
from django.shortcuts import render_to_response
import os


def index(request):
    return render_to_response("index.html", locals())
	
	
def get_right_order(ROOT):
    file_order_list = []
    final_mtime_order_list = []
    mtime_order_list = []
    right_mtime_order_list = []
    for i in os.listdir(ROOT):
        if os.path.isfile(os.path.join(ROOT, i)):
            mtime_order_list.append(os.stat(os.path.join(ROOT,i)).st_ctime)
            file_order_list.append(i)
    right_order_list = sorted(mtime_order_list)

    for record in right_order_list:
        order_list_index = mtime_order_list.index(record)
        final_mtime_order_list.append(order_list_index)

    for i in final_mtime_order_list:
        right_mtime_order_list.append(file_order_list[i])

    for i in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT,i)):
            right_mtime_order_list.append(i)
    return right_mtime_order_list[::-1]
	
	
#BluFab

def blufab_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\BluFab9"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/BluFab9"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())



	
	
def blufab_release_package(request):
    
    ROOT = "F:\\DVDFab_package\\Release_Package\\BluFab9\\Win"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/BluFab9/Win"
    platform = os.path.split(ROOT)[1].upper()
    right_mtime_order_list = get_right_order(ROOT)
    index_path = http_path.split("9000/")[1]
    all_files = right_mtime_order_list
    return render_to_response("display.html", locals())
	

def blufab_crash_dump(request):
    ROOT = "F:\\DVDFab_Dump\\BluFab"
    http_path = "http://10.10.2.72:9000/DVDFab_Dump/BluFab"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())
	
	
def mac_blufab_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Mac\\BluFab9"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Mac/BluFab9"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())
	
def mac_blufab_release_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\BluFab9\\Mac"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/BluFab9/Mac"
    platform = os.path.split(ROOT)[1].upper()
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
	
	
#DVDFab	
def dvdfab_developer_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Developer\\Win\\DVDFab9_mobile2"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Developer/Win/DVDFab9_mobile2"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())



def dvdfab_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\DVDFab9_mobile2"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/DVDFab9_mobile2"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())
	
	

def safedvdcopy(request):
    
    ROOT = "F:\\DVDFab_package\\Release_Package\\DVDFab9\\Win\\SafeDVDCopy"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/DVDFab9/Win/SafeDVDCopy"
    platform = os.path.split(ROOT)[1].upper()
    right_mtime_order_list = get_right_order(ROOT)
    index_path = http_path.split("9000/")[1]
    all_files = right_mtime_order_list
    platform = "other"
    return render_to_response("display.html", locals())

	
	
def dvdfab_release_package(request):
    
    ROOT = "F:\\DVDFab_package\\Release_Package\\DVDFab9\\Win"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/DVDFab9/Win"
    #all_files = os.listdir(ROOT)[::-1]
    """
    for i in os.listdir(ROOT):
        if os.path.isfile(os.path.join(ROOT, i)):
            mtime_order_list.append(os.stat(os.path.join(ROOT,i)).st_ctime)
            file_order_list.append(i)
    right_order_list = sorted(mtime_order_list)

    for record in right_order_list:
        order_list_index = mtime_order_list.index(record)
        final_mtime_order_list.append(order_list_index)

    for i in final_mtime_order_list:
        right_mtime_order_list.append(file_order_list[i])

    for i in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT,i)):
            right_mtime_order_list.append(i)
    """
    platform = os.path.split(ROOT)[1].upper()
    right_mtime_order_list = get_right_order(ROOT)
    index_path = http_path.split("9000/")[1]
    all_files = right_mtime_order_list
    return render_to_response("display.html", locals())
	
	
def dvdfab_official_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\DVDFab9\\Win\\official"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/DVDFab9/Win/official"
    index_path = http_path.split("9000/")[1]
    all_files = get_right_order(ROOT)
    return render_to_response("dvdfab_official_package.html", locals())
	
	
def dvdfab_crash_dump(request):
    ROOT = "F:\\DVDFab_Dump\\DVDFab"
    http_path = "http://10.10.2.72:9000/DVDFab_Dump/DVDFab"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())
	
	
def mac_dvdfab_developer_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Developer\\Mac\\DVDFab9"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Developer/Mac/DVDFab9"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())
	

def mac_dvdfab_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Mac\\DVDFab9"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Mac/DVDFab9"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    platform = "other"
    return render_to_response("display.html", locals())
	
def mac_dvdfab_release_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\DVDFab9\\Mac"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/DVDFab9/Mac"
    platform = os.path.split(ROOT)[1].upper()
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def mac_dvdfab_official_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\DVDFab9\\Mac\\official"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/DVDFab9/Mac/official"
    platform = "other"
    index_path = http_path.split("9000/")[1]
    all_files = get_right_order(ROOT)
    return render_to_response("dvdfab_official_package.html", locals())

	
	
#DVDFab MediaPlayer2	
def player_release_package(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\DVDFabMediaPlayer2"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/DVDFabMediaPlayer2"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def player_crash_dump(request):
    ROOT = "F:\\DVDFab_Dump\\DVDFab_Media_Player"
    http_path = "http://10.10.2.72:9000/DVDFab_Dump/DVDFab_Media_Player"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def mac_player_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Mac\\DVDFabMediaPlayer2"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Mac/DVDFabMediaPlayer2"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def mac_player_release_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\DVDFabMediaPlayer2"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/DVDFabMediaPlayer2"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
	
	
#VidOn Server
def vidon_server_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\VDMServer"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/VDMServer"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def vidon_server_release_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\VDMServer"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/VDMServer"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1] 
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	

def vidon_server_crash_dump(request):
    ROOT = "F:\\DVDFab_Dump\\VDMServer"
    http_path = "http://10.10.2.72:9000/DVDFab_Dump/VDMServer"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
	

#VidOn XBMC
def vidon_xbmc_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\VDMMediaCenter"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/VDMMediaCenter"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	

def linux_vbox1_package(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\vbox1\\Vidonme_mediacenter"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/vbox1/Vidonme_mediacenter"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())

def linux_vidon_xbmc_av500_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\VidOn.me TV apk\\AV500"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/VidOn.me TV apk/AV500"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())

	
def linux_vidon_xbmc_daily_build(request):
    ROOT = "F:\\DVDFab_package\\daily_build\\Win\\VidOn.me TV apk"
    http_path = "http://10.10.2.72:9000/DVDFab_package/daily_build/Win/VidOn.me TV apk"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
	
def linux_vidon_xbmc_release_package(request):
    ROOT = "F:\\DVDFab_package\\Release_Package\\VidOn.me TV apk"
    http_path = "http://10.10.2.72:9000/DVDFab_package/Release_Package/VidOn.me TV apk"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def linux_vidon_xbmc_crash_dump(request):
    ROOT = "F:\\DVDFab_Dump\\Android_Blu_ray_Box"
    http_path = "http://10.10.2.72:9000/DVDFab_Dump/Android_Blu_ray_Box"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
		
	
	
def vidonmemobile_android(request):
    ROOT = "F:\\DVDFab_package\\VidOn.me Mobile\\VidOn.meAndroidPlayer"
    http_path = "http://10.10.2.72:9000/DVDFab_package/VidOn.me Mobile/VidOn.meAndroidPlayer"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())
	
	
def vidonmemobile_ios(request):
    ROOT = "F:\\DVDFab_package\\VidOn.me Mobile\\VidOn.meIOSPlayer"
    http_path = "http://10.10.2.72:9000/DVDFab_package/VidOn.me Mobile/VidOn.meIOSPlayer"
    platform = "other"
    all_files = os.listdir(ROOT)[::-1]
    index_path = http_path.split("9000/")[1]
    return render_to_response("display.html", locals())


	

	
	
