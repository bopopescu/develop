from django.shortcuts import HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response("index.html")
	
def win_dvdfab_build(request):
    return render_to_response("win_dvdfab_build.html")
	
def mac_dvdfab_build(request):
    return render_to_response("mac_dvdfab_build.html")
	
def tdmore_build(request):
    return render_to_response("tdmore_build.html")
	
def safedvdcopy_build(request):
    return render_to_response("safedvdcopy_build.html")
	
def mac_safedvdcopy_build(request):
    return render_to_response("mac_safedvdcopy_build.html")
	
def mac_safedvdcopy_backup_build(request):
    return render_to_response("mac_safedvdcopy_backup_build.html")
	
def win_dvdfab_official_build(request):
    return render_to_response("win_dvdfab_official_build.html")
	
def mac_dvdfab_official_build(request):
    return render_to_response("mac_dvdfab_official_build.html")
	
	
def vidon_xbmc(request):
    return render_to_response("vidon_xbmc.html")
