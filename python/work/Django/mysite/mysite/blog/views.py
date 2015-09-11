#-*- coding:utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
import string
import time
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from forms import * 
from django.db.models import Q

import os
import subprocess
import tempfile, zipfile 
from django.core.servers.basehttp import FileWrapper

@csrf_exempt
def index(request):
    os.startfile('D:/DVDFab90/DVDFab.exe')
    cmd = 'D:/DVDFab90/DVDFab.exe /MODE "OPENSOURCE" /SRC "Z:/ELEMENTARY_S1_D3.iso" /DUMPSOURCEINFO "d:/test/xudedong/ELEMENTARY_S1_D3.iso.xml" /SILENCE /CLOSE'
    #cmd = "call D:/test/test.bat"
    subprocess.call(cmd, shell=True)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    result_out = p.stdout.read()
    result_err = p.stderr.read()
    fp = open("d:/test/test_out.txt","w")
    fp.write(result_out)
    fp.close()
    fp = open("d:/test/test_err.txt","w")
    fp.write(result_err)
    fp.close()
    
    return render_to_response('base.html') 

def new_add_case(request):
    Num = request.GET.get('Num','')
    Num_test_link = request.GET.get('Num_test_link','')
    Iso_type = request.GET.get('Iso_type','')
    Mode = request.GET.get('Mode','')
    Src_iso = request.GET.get('Src_iso','')
    Dest_type = request.GET.get('Dest_type','')
    Out_disc = request.GET.get('Out_disc','')
    Profile = request.GET.get('Profile','')
    Enable_2Dto3D = request.GET.get('Enable_2Dto3D','')
    Remove_HD_audio = request.GET.get('Remove_HD_audio','')
    
    Video_decoder_H264 = request.GET.get('Video_decoder_H264','')
    Video_decoder_VC1 = request.GET.get('Video_decoder_VC1','')    
    Video_decoder_MPEG2 = request.GET.get('Video_decoder_MPEG2','')
    Video_encoder_H264 = request.GET.get('Video_encoder_H264','')
    BD3D_convert_type = request.GET.get('BD3D_convert_type','')
    Compress_to_AC3 = request.GET.get('Compress_to_AC3','')
    DVDFab_description = request.GET.get('DVDFab_description','')
    Src_folder = request.GET.get('Src_folder','')
    Src_path = request.GET.get('Src_path','')
    
    Audio = request.GET.get('Audio','')
    Audio_type = request.GET.get('Audio_type','')
    Change_play_order = request.GET.get('Change_play_order','')
    Copy_IFO = request.GET.get('Copy_IFO','')
    Display_forced_sub = request.GET.get('Display_forced_sub','')
    Jump_menu = request.GET.get('Jump_menu','')
    Jump_main = request.GET.get('Jump_main','')
    
    Remove_DTS = request.GET.get('Remove_DTS','')
    Path_player = request.GET.get('Path_player','')
    Preserve_menu_disc2 = request.GET.get('Preserve_menu_disc2','')
    Remove_menu = request.GET.get('Remove_menu','')
    Remove_PGC = request.GET.get('Remove_PGC','')
    Rewind = request.GET.get('Rewind','')
    Subtitle = request.GET.get('Subtitle','')
    Title = request.GET.get('Title','')
    Volume = request.GET.get('Volume','')
    
    Num = Num.strip()
    Num_test_link = Num_test_link.strip()
    Iso_type = Iso_type.strip()
    Mode = Mode.strip()
    Src_iso = Src_iso.strip()
    Dest_type = Dest_type.strip()
    Out_disc = Out_disc.strip()
    Profile = Profile.strip()
    Enable_2Dto3D = Enable_2Dto3D.strip()
    Remove_HD_audio = Remove_HD_audio.strip()
    Video_decoder_H264 = Video_decoder_H264.strip()
    Video_decoder_VC1 = Video_decoder_VC1.strip()
    Video_decoder_MPEG2 = Video_decoder_MPEG2.strip()
    Video_encoder_H264 = Video_encoder_H264.strip()
    BD3D_convert_type = BD3D_convert_type.strip()
    Compress_to_AC3 = Compress_to_AC3.strip()
    DVDFab_description = DVDFab_description.strip()
    Src_folder = Src_folder.strip()
    Src_path = Src_path.strip()
    Audio = Audio.strip()
    Audio_type = Audio_type.strip()
    Change_play_order = Change_play_order.strip()
    Copy_IFO = Copy_IFO.strip()
    Display_forced_sub = Display_forced_sub.strip()
    Jump_menu = Jump_menu.strip()
    Jump_main = Jump_main.strip()
    Remove_DTS = Remove_DTS.strip()
    Path_player = Path_player.strip()
    Preserve_menu_disc2 = Preserve_menu_disc2.strip()
    Remove_menu = Remove_menu.strip()
    Remove_PGC = Remove_PGC.strip()
    Rewind = Rewind.strip()
    Subtitle = Subtitle.strip()
    Title = Title.strip()
    Volume = Volume.strip()
    
    case = Case(Num = Num, Num_test_link = Num_test_link, Iso_type = Iso_type,Mode = Mode, Src_iso = Src_iso, Dest_type = Dest_type, Out_disc = Out_disc, Profile = Profile, Enable_2Dto3D = Enable_2Dto3D, \
               Remove_HD_audio = Remove_HD_audio, Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1, Video_decoder_MPEG2 = Video_decoder_MPEG2, \
               Video_encoder_H264 = Video_encoder_H264, BD3D_convert_type = BD3D_convert_type, Compress_to_AC3 = Compress_to_AC3, DVDFab_description = DVDFab_description, Src_folder = Src_folder, \
               Src_path = Src_path, Audio = Audio, Audio_type = Audio_type, Change_play_order = Change_play_order, Copy_IFO = Copy_IFO, Display_forced_sub = Display_forced_sub, \
               Jump_menu = Jump_menu, Jump_main = Jump_main, Remove_DTS= Remove_DTS, Path_player = Path_player, Preserve_menu_disc2 = Preserve_menu_disc2, Remove_menu = Remove_menu, \
               Remove_PGC = Remove_PGC, Rewind = Rewind, Subtitle = Subtitle, Title = Title, Volume = Volume)
    if Num:
        case.save()
        return HttpResponseRedirect('/case/')
    return render_to_response('new_case.html',locals())
 
 
def new_add_client(request):
     PC_name = request.POST.get('PC_name','')
     PC_ip = request.POST.get('PC_ip','')
     Dvdfab_path = request.POST.get('Dvdfab_path','')
     Dest_path = request.POST.get('Dest_path','')
     
     PC_name = PC_name.strip()
     PC_ip = PC_ip.strip()
     Dvdfab_path = Dvdfab_path.strip()
     Dest_path = Dest_path.strip()
     
     client = Client(PC_name = PC_name, PC_ip = PC_ip, Dvdfab_path = Dvdfab_path, Dest_path = Dest_path)
     context = {'request':request,
                'PC_name':PC_name,
                'PC_ip':PC_ip,
                'Dvdfab_path':Dvdfab_path,
                'Dest_path':Dest_path,
                'client':client             
                }
     if PC_name and PC_ip :
         client.save()
         return HttpResponseRedirect('/client/')
     return render_to_response('new_client.html',context,context_instance=RequestContext(request))
 
 
def new_add_BD(request):
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Numbers_jar = Numbers_jar.strip()
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
    bd = Samples(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
            Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    if Name:
        bd.save()
        return HttpResponseRedirect('/bd_samples/')
    return render_to_response('new_BD.html',locals())
 
 
def new_add_DVD(request):
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
   
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
    dvd = DVD_samples(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
                 Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    if Name:
        dvd.save()
        return HttpResponseRedirect('/dvd_samples/')
    return render_to_response('new_DVD.html', locals()) 
 
 
 
def new_add_BD3D(request):
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Numbers_jar = Numbers_jar.strip()
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
    bd3d = BD3D_samples(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
            Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    if Name:
        bd3d.save()
        return HttpResponseRedirect('/bd3d_samples/')
    return render_to_response('new_BD3D.html',locals())


def new_add_version(request):
    Version = request.POST.get('Version','')
    Create_time = request.POST.get('Create_time','')
    Description = request.POST.get('Description','')
    Notes = request.POST.get('Notes','')
    
    Version = Version.strip()
    Create_time = Create_time.strip()
    Description = Description.strip()
    Notes = Notes.strip()
    
    version = Versions(Version = Version, Create_time = Create_time, Description = Description, Notes = Notes)
    context = {'request':request,
           'Version':Version,
           'Create_time':Create_time,
           'Description':Description,
           'Notes':Notes,
           'version':version           
           }
    
    if Version:
        version.save()
        return HttpResponseRedirect('/version/')
    return render_to_response('new_version.html',context, context_instance=RequestContext(request))


def case(request):
    case_type = request.GET.get('case_type','')
    client = Client.objects.all().order_by("PC_name")
    version = Versions.objects.all()[0:3]
    
    #Blu_Copy
    if case_type == 'Blu_Copy':   
        qs = Case.objects.filter(Q(Mode__iexact = 'fulldisc') | Q(Mode__iexact = 'mainmovie')).order_by('Num') 
        case = qs.filter(Q(Iso_type__iexact = 'BD')).order_by("Num")   
    elif case_type == 'BC_P0_2':
        qs = Case.objects.filter(Num__gte = '026').order_by('Num')
        case = qs.filter(Num__lte = '050')     
    elif case_type == 'BC_P1_1':
        qs = Case.objects.filter(Num__gte = '051').order_by('Num')
        case = qs.filter(Num__lte = '076')
    elif case_type == "BC_P1_2":
        qs = Case.objects.filter(Q(Mode = "bdfulldisc") | Q(Mode = "bdmainmovie")).order_by("Num")
        qs1 = qs.filter(Num__gte = "101")
        case = qs1.filter(Num__lte = "125")              
    elif case_type == 'BC_P1_3':
        qs = Case.objects.filter(Num__gte = '701').order_by('Num')
        case = qs.filter(Num__lte = '730')    
    elif case_type == 'BC_P2':
        qs = Case.objects.filter(Num__gte = "151").order_by("Num")
        case = qs.filter(Num__lte = "175")
    elif case_type == 'BC_P3':
        qs = Case.objects.filter(Num__gte = "176").order_by("Num")
        case = qs.filter(Num__lte = "200")
    
    #Blu_ Ripper    
    elif case_type == 'Blu_Ripper':
        case = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num") 
        #case = qs.exclude(Q(Mode__icontains = "dvd") | Q(Mode__icontains = "3d")).order_by("Num")      
    elif case_type == "BR_P0":
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num")
        qs1 = qs.filter(Num__gte = "201").order_by("Num")
        case = qs1.filter(Num__lte = "290")       
    elif case_type == "BR_P1":
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num")
        qs1 = qs.filter(Num__gte = "291").order_by("Num")
        case = qs1.filter(Num__lte = "380")    
    elif case_type == "BR_P2":
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num")
        qs1 = qs.filter(Num__gte = "381").order_by("Num")
        case = qs1.filter(Num__lte = "400")   
    
    #DVD_Copy        
    elif case_type == 'DVD_Copy':
        qs = Case.objects.filter(Q(Mode__iexact = "fulldisc") | Q(Mode__iexact = "mainmovie")).order_by("Num")
        case = qs.filter(Q(Iso_type__iexact = 'DVD')).order_by("Num")
    elif case_type == 'DC_P0':
        qs = Case.objects.filter(Num__gte = "601").order_by("Num")
        case = qs.filter(Num__lte = "620")

    #DVD_Ripper        
    elif case_type == 'DVD_Ripper':
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type = "DVD")).order_by("Num")
        case = qs.filter(Q(Num__gte = "401") & Q(Num__lte = "600")).order_by("Num")    
    elif case_type == 'DR_P0':
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type = "DVD")).order_by("Num")
        qs1 = qs.filter(Num__gte = "401").order_by("Num")
        case = qs1.filter(Num__lte = "500")
    elif case_type == 'DR_P1':
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type = "DVD")).order_by("Num")
        qs1 = qs.filter(Num__gte = "501").order_by("Num")
        case = qs1.filter(Num__lte = "600")
        

   
    #Blu_DVD
    elif case_type == 'Blu_DVD':
        cae = Case.objects.filter(Q(Mode__iexact = "bluraydvd")).order_by("Num")
        case = Case.objects.filter(Q(Num__gte = "801") & Q(Num__lte = "824")).order_by("Num") 
    elif case_type == 'BD_P0':
        qs = Case.objects.filter(Num__gte = "801").order_by("Num")
        case = qs.filter(Num__lte = "824")    
    #elif case_type == 'BD_P1':
    #    qs = Case.objects.filter(Num__gte = "801").order_by("Num")
    #    case = qs.filter(Num__lte = "824")    
    #elif case_type == 'BD_P2':
    #    qs = Case.objects.filter(Num__gte = "801").order_by("Num")
    #    case = qs.filter(Num__lte = "824")
    
    #Blu_3D        
    elif case_type == 'Blu_3D':
        case = Case.objects.filter(Q(Mode__icontains = "bluray3d")).order_by("Num")  
        #case = qs.filter(Q(Num__gte = "901") & Q(Num__lte = "950"))
    elif case_type == 'B3_P0':
        qs = Case.objects.filter(Num__gte = "901").order_by("Num")
        case = qs.filter(Num__lte = "950")       
    elif case_type == 'B3_P1':
        qs = Case.objects.filter(Num__gte = "901").order_by("Num")
        case = qs.filter(Num__lte = "950")
   
    #VideoConterver        
    elif case_type == 'VideoConverter':
        case = Case.objects.filter(Q(Mode__icontains = "Converter")).order_by("Num")  
    elif case_type == 'VC_P0':
        qs = Case.objects.filter(Q(Mode__icontains = "Converter")).order_by("Num")
        qs1 = qs.filter(Num__gte = "1000")
        case = qs1.filter(Num__lte = "1100")     
    #elif case_type == 'VC_P1':
    #    qs = Case.objects.filter(Q(Mode__icontains = "video")).order_by("Num")
    #    qs1 = qs.filter(Num__gte = "1051")
    #    case = qs1.filter(Num__lte = "1100")

    #2Dto3D
    elif case_type == '2Dto3D':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        qs1 = qs.filter(Num__gte = "1101")
        case = qs1.filter(Num__lte = "1399")          
    elif case_type == '2T3_DR':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        qs1 = qs.filter(Num__gte = "1101")
        case = qs1.filter(Num__lte = "1199")     
    elif case_type == '2T3_BR':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        qs1 = qs.filter(Num__gte = "1201")
        case = qs1.filter(Num__lte = "1299")
    elif case_type == '2T3_VC':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        qs1 = qs.filter(Num__gte = "1301")
        case = qs1.filter(Num__lte = "1399")
    
    #Mini_test_set
    elif case_type == 'Mini_test_set':  
        qs = Case.objects.filter(Q(Iso_type__iexact = '') ).order_by('Num')
        case = qs.filter(Q(Num__gte = "2001") & Q(Num__lte = "2400")).order_by("Num") 
    elif case_type == "3D_Anaglyph":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2001") & Q(Num__lte = "2050")).order_by("Num")    
    elif case_type == "3D_Split":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2051") & Q(Num__lte = "2100")).order_by("Num")
    elif case_type == "3D_TwoFiles":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2101") & Q(Num__lte = "2150")).order_by("Num")
    elif case_type == "3D_TwoVideos":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2151") & Q(Num__lte = "2200")).order_by("Num")
    elif case_type == "3D_Device":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2201") & Q(Num__lte = "2250")).order_by("Num")
    elif case_type == "DTS/LPCM_AC3":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2251") & Q(Num__lte = "2300")).order_by("Num")
    elif case_type == "BD_SBS":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2301") & Q(Num__lte = "2350")).order_by("Num")
    elif case_type == "BD_Blu":
        qs = Case.objects.filter(Q(Iso_type__iexact = '')).order_by('Num')
        case = qs.filter(Q(Num__gte = "2351") & Q(Num__lte = "2400")).order_by("Num")
    
    #BDCreator
    elif case_type == 'BDCreator':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        case = qs.filter(Q(Num__gte = "4012") & Q(Num__lte = "4029"))

    elif case_type == 'BDC_P0':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        qs1 = qs.filter(Num__gte = "4012")
        case = qs1.filter(Num__lte = "4029")     
    #elif case_type == 'BDC_P1':
    #    qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
    #    qs1 = qs.filter(Num__gte = "4051")
    #    case = qs1.filter(Num__lte = "4100")
        
    #DVDCreator
    elif case_type == 'DVDCreator':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        case = qs.filter(Q(Num__gte = "4000") & Q(Num__lte = "4011"))

    elif case_type == 'DVD_DVD5':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        qs1 = qs.filter(Num__gte = "4000")
        case = qs1.filter(Num__lte = "4005")     
    elif case_type == 'DVD_DVD9':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        qs1 = qs.filter(Num__gte = "4006")
        case = qs1.filter(Num__lte = "4011")
               
    else:
        qs = Case.objects.filter(Num__gte = "001").order_by("Num")
        case = qs.filter(Num__lte = "025")
    
    return render_to_response('case.html', locals())

@csrf_exempt  
def insert_session(request):  

        checkbox = request.POST.getlist('checkbox')
        #return HttpResponse(checkbox)
        pc_name_list = request.POST.getlist('pc_name')
        dvdfab_path_list = request.POST.getlist('dvdfab_path')
        num_list = request.POST.getlist('num')
        select_version_list = request.POST.getlist('select_version')
        Start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_time = Start_time.replace('-','_')
        start_time = start_time.replace(':','_')
        path = start_time.replace(' ','_')
        #return HttpResponse(checkbox)
        #return HttpResponse(num_list)
        for num in checkbox :
            index = num_list.index(num)
            PC_name = pc_name_list[index]   
 
            Dvdfab_path = dvdfab_path_list[index]
            Version = select_version_list[index]   
            client_dest_path = Client.objects.filter(PC_name = PC_name).values()[0]['Dest_path']
            case = Case.objects.get(Num = num) 

            Num = case.Num
            Iso_type = case.Iso_type
            Mode = case.Mode
            
            Out_disc = case.Out_disc
            Remove_HD_audio = case.Remove_HD_audio
            BD3D_convert_type = case.BD3D_convert_type
            Compress_to_AC3 = case.Compress_to_AC3
            
            Video_decoder_H264 = case.Video_decoder_H264
            Video_decoder_VC1 = case.Video_decoder_VC1
            Video_decoder_MPEG2 = case.Video_decoder_MPEG2
            
            Video_encoder_H264 = case.Video_encoder_H264
            Profile = case.Profile
            Enable_2Dto3D = case.Enable_2Dto3D
   
            Src_iso = case.Src_iso
            Src_folder = case.Src_folder  
            #Dest_type = case.Dest_type
            Audio = case.Audio
            Audio_type = case.Audio_type
    
            Change_play_order = case.Change_play_order
            Copy_IFO = case.Copy_IFO
            Display_forced_sub = case.Display_forced_sub
            Jump_menu = case.Jump_menu
            Jump_main = case.Jump_main
   
            Path_player = case.Path_player
            Preserve_menu_disc2 = case.Preserve_menu_disc2
            Remove_DTS = case.Remove_DTS

            Remove_menu = case.Remove_menu
            Remove_PGC = case.Remove_PGC
            Rewind = case.Rewind
            Subtitle = case.Subtitle 
            Title = case.Title 
            Volume =case.Volume
    
            Num_test_link =  case.Num_test_link
            '''
            if Mode.upper().startswith('BD') or Mode.upper().startswith('BLURAY'):
                Src_path = '/U_nas/volume1/bd/' + case.Src_iso
                
            elif Mode.upper().startswith('DVD') or Mode.upper().startswith('FULLDISC'):
                Src_path = '/U_nas/volume2/dvd/' + case.Src_iso
            else:
                Src_path = '/U_nas/volume3/video/' + case.Src_iso
            '''
            if Iso_type.upper() == 'BD':
                Src_path = '/U_nas/volume1/bd/' + case.Src_iso
            elif Iso_type.upper() == 'DVD':
                Src_path = '/U_nas/volume2/dvd/' + case.Src_iso
            else:
                Src_path = '/U_nas/volume3/video/' + case.Src_iso
                
            Start_time = time.strftime('%Y-%m-%d %H:%M:%S')
            Sub_num = ''
            End_time = '' 
            Total_time = ''
            
            Web_log_path = ''
            Log_folder_path = ''
            Dvdfab_path = ''  
            Current_src_path = '' 
            
            Folder_size = ''
            DVDFab_description = case.DVDFab_description
            Result = ''
            Developer = ''
            Flag = 0
            Dest_path = ''          
            session = Session(PC_name = PC_name, Num = Num, Iso_type = Iso_type, Mode = Mode, Out_disc = Out_disc, Remove_HD_audio = Remove_HD_audio, BD3D_convert_type = BD3D_convert_type,\
                             Compress_to_AC3 = Compress_to_AC3, Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1,\
                             Video_decoder_MPEG2 = Video_decoder_MPEG2, Video_encoder_H264 = Video_encoder_H264, Profile =Profile, Enable_2Dto3D = Enable_2Dto3D,\
                             Audio = Audio, Audio_type = Audio_type, Change_play_order = Change_play_order, Dvdfab_path = Dvdfab_path, Current_src_path = Current_src_path,\
                             Copy_IFO = Copy_IFO, Display_forced_sub = Display_forced_sub, Jump_menu = Jump_menu, Jump_main = Jump_main, Path_player = Path_player,\
                             Preserve_menu_disc2 = Preserve_menu_disc2,  Remove_DTS =  Remove_DTS, Remove_menu = Remove_menu, Remove_PGC = Remove_PGC, Rewind = Rewind,\
                             Subtitle = Subtitle, Dest_path = Dest_path,Title = Title, Volume = Volume, Sub_num = Sub_num, Web_log_path = Web_log_path, Log_folder_path = Log_folder_path,\
                             Src_path = Src_path, Start_time = Start_time, End_time = End_time, Total_time = Total_time, Folder_size =Folder_size,\
                             DVDFab_description = DVDFab_description, Result= Result, Developer = Developer, Flag = Flag)
            session.save()  
         
            session = Session.objects.filter(Num = num)[0]
            
            if case.Dest_type.upper() == 'ISO':
                #Dest_path = client_dest_path + '/' + path  + '_' + num + '/'+case.Src_iso
                if '/' in client_dest_path:
                    if client_dest_path.endswith('/'):
                        Dest_path = client_dest_path + str(session.id) + '_'+ path  + '_' + num + '/'+case.Src_iso
                    else:
                        Dest_path = client_dest_path + '/' + str(session.id) + '_'+ path  + '_' + num + '/'+case.Src_iso
                elif '\\' in client_dest_path:     
                    if client_dest_path.endswith('\\'):
                        Dest_path = client_dest_path + str(session.id) + '_'+ path  + '_' + num + '\\'+case.Src_iso
                    else:
                        Dest_path = client_dest_path + '\\' + str(session.id) + '_'+ path  + '_' + num + '\\'+case.Src_iso
                else:
                    Dest_path = client_dest_path + '/' + str(session.id) + '_'+ path  + '_' + num + '/'+case.Src_iso
                    
            else: 
                if '/' in client_dest_path:
                    if client_dest_path.endswith('/'):
                        Dest_path = client_dest_path + str(session.id) + '_'+ path  + '_' + num
                    else:
                        Dest_path = client_dest_path + '/' + str(session.id) + '_'+ path  + '_' + num
                elif '\\' in client_dest_path:     
                    if client_dest_path.endswith('\\'):
                        Dest_path = client_dest_path + str(session.id) + '_'+ path  + '_' + num
                    else:
                        Dest_path = client_dest_path + '\\' + str(session.id) + '_'+ path  + '_' + num
                else:
                    Dest_path = client_dest_path + '/' + str(session.id) + '_'+ path  + '_' + num
            #Dest_path = Dest_path.replace('/','\\')
            session.Dest_path = Dest_path
            session.save()
        return  HttpResponseRedirect('/case/') 
                

def client(request):
    client = Client.objects.all()
    #client = Client.objects.all().values()[1] 
    return render_to_response('client.html', locals())


def version(request):  
    version = Versions.objects.all()
    return render_to_response('version.html', locals())


def bd_samples(request):  
    bd = Samples.objects.all()
    return render_to_response('BD.html', locals())


def dvd_samples(request):    
    dvd = DVD_samples.objects.all()
    return render_to_response('DVD.html', locals())


def bd3d_samples(request):   
    bd3d = BD3D_samples.objects.all()
    return render_to_response('BD3D.html', locals())


def all_samples(request):  
    bd_samples = Samples.objects.all()
    dvd_samples = DVD_samples.objects.all()
    bd3d_samples = BD3D_samples.objects.all()
    return render_to_response('all.html', locals())


def session(request): 
    nowpage = request.GET.get('nowpage','')
    if nowpage == '':
        nowpage = 1
    else:
        nowpage = int(nowpage)
    count = Session.objects.count()
    if count % 100 == 0:
        pageall = count / 100
    else:
        pageall = count / 100 + 1
    if nowpage - 1 < 1:
        pageup = 1
    else:
        pageup = nowpage - 1
    if nowpage + 1 >= pageall:
        pagedn = pageall
    else:
        pagedn = nowpage + 1
    start = 100*(nowpage - 1)    
    session = Session.objects.all().order_by('-id')[start:(start + 100)]
    return render_to_response('session.html', locals())

 
def search_session(request):
    api = request.GET.get('api','')         #index, Mode, PC_name, Num, Result ....
    api_name = request.GET.get('api_name','')
    sample_name = request.GET.get('sample_name','')
    api_name = api_name.strip()
    sample_name = sample_name.strip()
 
    '''
    if Mode.upper().startswith('BD') or Mode.upper().startswith('BLURAY'):
        Src_path = '/U_nas/volume1/bd/' + case.Src_iso           
    elif Mode.upper().startswith('DVD') or Mode.upper().startswith('FULLDISC'):
        Src_path = '/U_nas/volume2/dvd/' + case.Src_iso
    else:
        Src_path = '/U_nas/volume3/video/' + case.Src_iso
    '''
 
    if api == 'id' and api_name:
        session = Session.objects.extra(where = ["id like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
    
    elif api == 'Mode' and api_name:
        session = Session.objects.extra(where = ["Mode like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
                
    elif api == 'Src_path' and api_name:
        session = Session.objects.extra(where = ["Src_path like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
        
    elif api == 'Num' and api_name:
        session = Session.objects.extra(where = ["Num like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
    
    elif api == 'Result' and api_name:
        session = Session.objects.extra(where = ["Result like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
        
    elif api == 'Out_disc' and api_name:
        session = Session.objects.extra(where = ["Out_disc like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
        
    elif api == 'PC_name' and api_name:
        session = Session.objects.extra(where = ["PC_name like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
        
    elif api == 'Profile' and api_name:
        session = Session.objects.extra(where = ["Profile like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
        
    elif api == 'Developer' and api_name:
        session = Session.objects.extra(where = ["Developer like'%%"+ str(api_name) + "%%'"])
        if not session:
            return render_to_response('error.html')
    else:
        return HttpResponseRedirect('/session/')
    return render_to_response('session.html',locals())
 
 
def search_DVD(request):  
    dvd = DVD_samples.objects.all()
    return render_to_response('search_DVD.html',locals()) 

 
def search_BD(request):
    bd = Samples.objects.all()
    return render_to_response('search_BD.html',locals())


def search_3D(request):
    bd3d = BD3D_samples.objects.all()
    return render_to_response('search_BD3D.html',locals())


def search_File(request):
    return render_to_response('search_File.html',locals())

@csrf_exempt
def test_result(request):
    list = []
    list_str_int = []
    day_info_list = []
    days_info_list = []
    PC_name = request.POST.get('PC_name', '').strip()
    check_Flag = request.POST.get('check_Flag', '').strip()
    ziduan = request.GET.get('ziduan','')
    test_api = request.POST.get('test_api','')
    test_name = request.POST.get('test_name','').strip()
    Flag = request.POST.get('Flag','').strip()
    Flag_old = request.POST.get('Flag_old','').strip()
    
    update_flag_from_day = request.POST.get('update_flag_from_day','').strip()
    update_flag_to_day = request.POST.get('update_flag_to_day','').strip()
    PC_name_by_day = request.POST.get('PC_name_by_day', '').strip()
    Flag_old_by_day = request.POST.get('Flag_old_by_day','').strip()
    Flag_by_day = request.POST.get('Flag_by_day','').strip()
    
    if '/' in update_flag_from_day:
        update_flag_from_day = update_flag_from_day.replace('/','-')
    if '.' in test_name:
        update_flag_from_day = update_flag_from_day.replace('.','-')
    if ',' in test_name:
        update_flag_from_day = update_flag_from_day.replace(',','-')
    
    if '/' in update_flag_to_day:
        update_flag_to_day = update_flag_to_day.replace('/','-')
    if '.' in test_name:
        update_flag_to_day = update_flag_to_day.replace('.','-')
    if ',' in test_name:
        update_flag_to_day = update_flag_to_day.replace(',','-')
    
    
    client = Client.objects.all().order_by('PC_name') 
    days = request.POST.get('days','').strip()
    if days:  
        try:
            days = int(days)      
        except Exception:
            pass     
        else:
            if days == 0:
                pass
            else:
                web = Web_params(Days_display = days)   
                web.save()
            
    if test_api == 'id' and test_name: 
        test_name = test_name.split(',') 
        for i in test_name:
            if '-' in i:
                list_index = i.split('-')
                for i in range(int(list_index[0]),int(list_index[1]) + 1):
                    list_str_int.append(i) 
            elif '~' in i:
                list_index = i.split('~')
                for i in range(int(list_index[0]),int(list_index[1]) + 1):
                    list_str_int.append(i)           
            else:
                i = int(i)
                list_str_int.append(i)       
        for i in list_str_int:
            qs = Session.objects.filter(id = i)
            if Flag_old:
                session = qs.filter(Flag = Flag_old)
            else:
                session = qs
            if Flag:
                session.update(Flag = Flag)        
            #if not session:
            #    return render_to_response('error.html')  
    elif test_api == 'PC_name' and test_name:      
        test_name = test_name.split(',')
        for i in test_name:
            qs = Session.objects.filter(PC_name = i)    
            if Flag_old:
                session = qs.filter(Flag = Flag_old)
            else:
                session = qs
            if Flag:
                session.update(Flag = Flag)        
            #if not session:
            #    return render_to_response('error.html')        
    elif test_api == 'Init_time' and test_name:      
        if '/' in test_name:
            test_name = test_name.replace('/','-')
        if '.' in test_name:
            test_name = test_name.replace('.','-')
        if ',' in test_name:
            test_name = test_name.replace(',','-')
            
        qs = Session.objects.filter(Init_time = test_name)  
        if Flag_old:
            session = qs.filter(Flag = Flag_old)
        else:
            session = qs  
        if Flag:
            session.update(Flag = Flag)  
        #if not session:
        #    return render_to_response('error.html')  
    elif test_api == 'Flag_1':
        #if test_name: 
        #    qs = Session.objects.filter(Flag = int(test_name))
        #else:
        #    qs = Session.objects.all()
        if Flag_old:
            session = Session.objects.filter(Flag = Flag_old)
        else:
            session = Session.objects.all()
        if Flag:
            session.update(Flag = Flag)
            #if not session:
            #    return render_to_response('error.html')   
    else:
        pass
    
    if update_flag_from_day:
        qs = Session.objects.filter(Init_time__gte = update_flag_from_day)
        if update_flag_to_day:
            qs0 = qs.filter(Init_time__lte = update_flag_to_day)
        else:
            qs0 = qs
        if PC_name_by_day:
            qs1 = qs0.filter(PC_name = PC_name_by_day)
        else:
            qs1 = qs0
        if Flag_old_by_day:
            session = qs1.filter(Flag = Flag_old_by_day)
        else:
            session = qs1
        if Flag_by_day:
            session.update(Flag = Flag_by_day)
            
    web_params = Web_params.objects.all() 
    if web_params:  
        days = int(web_params[0].Days_display)     
    else:
        days = 7
        
    now_day = datetime.datetime.now()
    for day in range(days):   
        if ziduan == 'Index':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('id')
        elif ziduan == 'Num':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Num')
        elif ziduan =='Mode':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Mode')
        elif ziduan == 'PC_name':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('PC_name')
        elif ziduan == 'Out_disc':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Out_disc')
        elif ziduan == 'Remove_HD_audio':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Remove_HD_audio')
        elif ziduan == 'BD3D_convert_type':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('BD3D_convert_type')
        elif ziduan == 'Compress_to_AC3':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Compress_to_AC3')
        elif ziduan == 'Video_decoder_H264':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Video_decoder_H264')
        elif ziduan == 'Video_decoder_VC1':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Video_decoder_VC1')
        elif ziduan == 'Video_decoder_MPEG2':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Video_decoder_MPEG2')
        elif ziduan == 'Video_encoder_H264':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Video_encoder_H264')
        elif ziduan == 'Enable_2Dto3D':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Enable_2Dto3D')
        elif ziduan == 'Profile':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Profile')
        elif ziduan == 'Src_path':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Src_path')
        elif ziduan == 'Dest_path':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Dest_path')
        elif ziduan == 'Start_time':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Start_time')
        elif ziduan == 'End_time':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('End_time')
        elif ziduan == 'Total_time':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Total_time')
        elif ziduan == 'Folder_size':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Folder_size')
        elif ziduan == 'DVDFab_description':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('DVDFab_description')
        elif ziduan == 'Result':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Result')
        elif ziduan == 'Developer':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Developer')
        elif ziduan == 'Flag':
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('Flag')
        else:
            session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day))
        if PC_name:
            session1 = session.filter(PC_name = PC_name) 
            #if not session1:
            #    return render_to_response('error.html') 
        else:
            session1 = session  
        if check_Flag:
            session2 = session1.filter(Flag = check_Flag)
        else:
            session2 = session1
        if session2:
            
            day_info_list.append([session[0].Init_time,session2])
    
    return render_to_response('test_result.html',locals())
 
    
def search_test_result(request):  
    
    day_info_list = []
    days_info_list = []

    test_api = request.GET.get('test_api','')
    test_name = request.GET.get('test_name','')
    Flag = request.GET.get('Flag','')
    test_name = test_name.strip() 
    Flag = Flag.strip()
    days = request.GET.get('days','')
    days = days.strip()
     
    if days != '':
        days = int(days)
        now_day = datetime.datetime.now()
        display_days = now_day - datetime.timedelta( days = days)
   
        for day in range(days):
            session1 = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day))
            if session1:
                day_info_list.append([session1[0].Init_time,session1])
        
    else:
        now_day = datetime.datetime.now()
        display_days = now_day - datetime.timedelta( days = 7)

        for day in range(7):
            session1 = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day))
            if session1:
                day_info_list.append([session1[0].Init_time,session1])
                
    if test_api == 'id' and test_name:  
        session = Session.objects.extra(where = ["id like '%%" + str(test_name) + "%%'"])  
        if Flag:
            session.update(Flag = Flag)
    
        if not session:
            return render_to_response('error.html')
              
    elif test_api == 'PC_name' and test_name:
        session = Session.objects.extra(where = ["PC_name like '%%" + str(test_name) + "%%'"])
        
        if Flag:
            session.update(Flag = Flag)
          
        if not session:
            return render_to_response('error.html')
        
    elif test_api == 'Init_time' and test_name:
        session = Session.objects.extra(where = ["Init_time like '%%" + str(test_name) + "%%'"])
        
        if Flag:
            session.update(Flag = Flag)
      
        if not session:
            return render_to_response('error.html')
        
    else:
        pass
       
    return render_to_response('search_test_result.html',locals())


@csrf_exempt
def search_type(request):
    client = Client.objects.all()
    version = Versions.objects.all()[0:3]
    search_type = request.POST.get('search_type','')
    type_context = request.POST.get('type_context','')
    type_context = type_context.strip()
    if search_type == 'Mode' and type_context:
        case = Case.objects.extra(where = ["Mode like'%%"+ str(type_context) + "%%'"])
        if not case:
            return render_to_response('error.html')   
    
    elif search_type == 'Src_iso' and type_context:
        case = Case.objects.extra(where = ["Src_iso like'%%"+ str(type_context) + "%%'"])
        if not case:
            return render_to_response('error.html')
    
    elif search_type == 'Out_disc' and type_context:
        case = Case.objects.extra(where = ["Out_disc like'%%"+ str(type_context) + "%%'"])
        if not case:
            return render_to_response('error.html')
    
    elif search_type == 'Profile' and type_context:
        case = Case.objects.extra(where = ["Profile like'%%"+ str(type_context) + "%%'"])
        if not case:
            return render_to_response('error.html')
         
    else:
        return HttpResponseRedirect('/case/')
 
    return render_to_response('case.html',locals(),context_instance = RequestContext(request))
 
 
def search_BD_type(request):
    BD = request.GET.get('BD','')
    BD_type = request.GET.get('BD_type','')
    BD_type = BD_type.strip()
    
    if BD == 'Name' and BD_type:
        bd = Samples.objects.extra(where = ["Name like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
       
    elif BD == 'Locations' and BD_type:
        bd = Samples.objects.extra(where = ["Locations like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
    
    elif BD == 'Video_info' and BD_type:
        bd = Samples.objects.extra(where = ["Video_info like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    elif BD == 'Audio_info' and BD_type:
        bd = Samples.objects.extra(where = ["Audio_info like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
    elif BD == 'Channel' and BD_type:
        bd = Samples.objects.extra(where = ["Channel like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    elif BD == 'Framerate' and BD_type:
        bd = Samples.objects.extra(where = ["Framerate like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    elif BD == 'Standard' and BD_type:
        bd = Samples.objects.extra(where = ["Standard like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    elif BD == 'Scan_type' and BD_type:
        bd = Samples.objects.extra(where = ["Scan_type like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    elif BD == 'Numbers_jar' and BD_type:
        bd = Samples.objects.extra(where = ["Numbers_jar like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    elif BD == 'Company' and BD_type:
        bd = Samples.objects.extra(where = ["Company like '%%" + str(BD_type) + "%%'"]) 
        if not bd:
            return render_to_response('error.html')
        
    else:
        return HttpResponseRedirect('/bd_samples/')
    return render_to_response('BD.html',locals()) 


def BD_sort(request):
    sort_name = request.GET.get('sort_name','')
    bd = Samples.objects.all().order_by(sort_name) 
    return render_to_response('BD.html',locals())


def search_DVD_type(request):
    DVD = request.GET.get('DVD','')
    DVD_type = request.GET.get('DVD_type','')
    DVD_type = DVD_type.strip()
    
    if DVD == 'Name' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Name like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
       
    elif DVD == 'Locations' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Locations like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
    
    elif DVD == 'Video_info' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Video_info like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
        
    elif DVD == 'Audio_info' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Audio_info like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
    elif DVD == 'Channel' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Channel like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
        
    elif DVD == 'Framerate' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Framerate like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
        
    elif DVD == 'Standard' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Standard like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
        
    elif DVD == 'Scan_type' and DVD_type:
        dvd = DVD_Samples.objects.extra(where = ["Scan_type like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
        
    elif DVD == 'Company' and DVD_type:
        dvd = DVD_samples.objects.extra(where = ["Company like '%%" + str(DVD_type) + "%%'"]) 
        if not dvd:
            return render_to_response('error.html')
        
    else:
        return HttpResponseRedirect('/dvd_samples/')
    return render_to_response('DVD.html',locals())


def DVD_sort(request):
    sort_name = request.GET.get('sort_name','')
    dvd = DVD_samples.objects.all().order_by(sort_name)
    
    return render_to_response('DVD.html',locals())


def search_BD3D_type(request):
    BD3D = request.GET.get('BD3D','')
    BD3D_type = request.GET.get('BD3D_type','')
    BD3D_type = BD3D_type.strip()
    
    if BD3D == 'Name' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Name like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
       
    elif BD3D == 'Locations' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Locations like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
    
    elif BD3D == 'Video_info' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Video_info like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    elif BD3D == 'Audio_info' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Audio_info like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
    elif BD3D == 'Channel' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Channel like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    elif BD3D == 'Framerate' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Framerate like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    elif BD3D == 'Standard' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Standard like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    elif BD3D == 'Scan_type' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Scan_type like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    elif BD3D == 'Numbers_jar' and BD3D_type:
        bd3d = BD3D_samples.objects.extra(where = ["Numbers_jar like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    elif BD3D == 'Company' and BD3D_type:
        bd = BD3D_samples.objects.extra(where = ["Company like '%%" + str(BD3D_type) + "%%'"]) 
        if not bd3d:
            return render_to_response('error.html')
        
    else:
        return HttpResponseRedirect('/bd3d_samples/')
    return render_to_response('BD3D.html',locals()) 


def BD3D_sort(request):
    sort_name = request.GET.get('sort_name','')
    bd3d = BD3D_samples.objects.all().order_by(sort_name)
    
    return render_to_response('BD3D.html',locals())


def search_all_type(request):
    All = request.GET.get('All','')
    all_type = request.GET.get('all_type','')
    all_type = all_type.strip()
    
    if All == 'Name' and all_type:
        bd = Samples.objects.extra(where = ["Name like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Name like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Name like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
       
    elif All == 'Locations' and all_type:
        bd = Samples.objects.extra(where = ["Locations like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Locations like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Locations like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
    
    elif All == 'Video_info' and all_type:
        bd = Samples.objects.extra(where = ["Video_info like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Video_info like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Video_info like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
        
    elif All == 'Audio_info' and all_type:
        bd = Samples.objects.extra(where = ["Audio_info like '%%" + str(all_type) + "%%'"])
        dvd = DVD_samples.objects.extra(where = ["Audio_info like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Audio_info like '%%" + str(all_type) + "%%'"]) 
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
    elif All == 'Channel' and all_type:
        bd = Samples.objects.extra(where = ["Channel like '%%" + str(all_type) + "%%'"])
        dvd = DVD_samples.objects.extra(where = ["Channel like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Channel like '%%" + str(all_type) + "%%'"]) 
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
        
    elif All == 'Framerate' and all_type:
        bd = Samples.objects.extra(where = ["Framerate like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Framerate like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Framerate like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
        
    elif All == 'Standard' and all_type:
        bd = Samples.objects.extra(where = ["Standard like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Standard like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Standard like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd and  not bd3d:
            return render_to_response('error.html')
        
    elif All == 'Scan_type' and all_type:
        bd = Samples.objects.extra(where = ["Scan_type like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Scan_type like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Scan_type like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd and not bd3d:
            return render_to_response('error.html')
        
    elif All == 'Numbers_jar' and all_type:
        bd = Samples.objects.extra(where = ["Numbers_jar like '%%" + str(all_type) + "%%'"]) 
        dvd = BD3DSamples.objects.extra(where = ["Numbers_jar like '%%" + str(all_type) + "%%'"])
        if not bd and not dvd:
            return render_to_response('error.html')
        
    elif All == 'Company' and all_type:
        bd = Samples.objects.extra(where = ["Company like '%%" + str(all_type) + "%%'"]) 
        dvd = DVD_samples.objects.extra(where = ["Company like '%%" + str(all_type) + "%%'"])
        bd3d = BD3D_samples.objects.extra(where = ["Company like '%%" + str(all_type) + "%%'"])
        if not bd and  not dvd and  not bd3d:
            return render_to_response('error.html')
        
    else:
        return HttpResponseRedirect('/all_samples/')
    return render_to_response('search_all_type.html',locals()) 
 
   
def update_case_page(request,param1):
    case = Case.objects.get(id = param1)
    return render_to_response('update_case.html',locals())   
   
   
def update_case(request,param1):   
    case = Case.objects.filter(id = param1)
    Num = request.GET.get('Num','')
    Num_test_link = request.GET.get('Num_test_link','')
    Iso_type = request.GET.get('Iso_type','')
    Mode = request.GET.get('Mode','')
    Src_iso = request.GET.get('Src_iso','')
    Dest_type = request.GET.get('Dest_type','')
    Out_disc = request.GET.get('Out_disc','')
    Profile = request.GET.get('Profile','')
    Enable_2Dto3D = request.GET.get('Enable_2Dto3D','')
    Remove_HD_audio = request.GET.get('Remove_HD_audio','')
    
    Video_decoder_H264 = request.GET.get('Video_decoder_H264','')
    Video_decoder_VC1 = request.GET.get('Video_decoder_VC1','')    
    Video_decoder_MPEG2 = request.GET.get('Video_decoder_MPEG2','')
    Video_encoder_H264 = request.GET.get('Video_encoder_H264','')
    BD3D_convert_type = request.GET.get('BD3D_convert_type','')
    Compress_to_AC3 = request.GET.get('Compress_to_AC3','')
    DVDFab_description = request.GET.get('DVDFab_description','')
    Src_folder = request.GET.get('Src_folder','')
    Src_path = request.GET.get('Src_path','')
    
    Audio = request.GET.get('Audio','')
    Audio_type = request.GET.get('Audio_type','')
    Change_play_order = request.GET.get('Change_play_order','')
    Copy_IFO = request.GET.get('Copy_IFO','')
    Display_forced_sub = request.GET.get('Display_forced_sub','')
    Jump_menu = request.GET.get('Jump_menu','')
    Jump_main = request.GET.get('Jump_main','')
    
    Remove_DTS = request.GET.get('Remove_DTS','')
    Path_player = request.GET.get('Path_player','')
    Preserve_menu_disc2 = request.GET.get('Preserve_menu_disc2','')
    Remove_menu = request.GET.get('Remove_menu','')
    Remove_PGC = request.GET.get('Remove_PGC','')
    Rewind = request.GET.get('Rewind','')
    Subtitle = request.GET.get('Subtitle','')
    Title = request.GET.get('Title','')
    Volume = request.GET.get('Volume','')
    
    Num = Num.strip()
    Num_test_link = Num_test_link.strip()
    Iso_type = Iso_type.strip()
    Mode = Mode.strip()
    Src_iso = Src_iso.strip()
    Dest_type = Dest_type.strip()
    Out_disc = Out_disc.strip()
    Profile = Profile.strip()
    Enable_2Dto3D = Enable_2Dto3D.strip()
    Remove_HD_audio = Remove_HD_audio.strip()
    Video_decoder_H264 = Video_decoder_H264.strip()
    Video_decoder_VC1 = Video_decoder_VC1.strip()
    Video_decoder_MPEG2 = Video_decoder_MPEG2.strip()
    Video_encoder_H264 = Video_encoder_H264.strip()
    BD3D_convert_type = BD3D_convert_type.strip()
    Compress_to_AC3 = Compress_to_AC3.strip()
    DVDFab_description = DVDFab_description.strip()
    Src_folder = Src_folder.strip()
    Src_path = Src_path.strip()
    Audio = Audio.strip()
    Audio_type = Audio_type.strip()
    Change_play_order = Change_play_order.strip()
    Copy_IFO = Copy_IFO.strip()
    Display_forced_sub = Display_forced_sub.strip()
    Jump_menu = Jump_menu.strip()
    Jump_main = Jump_main.strip()
    Remove_DTS = Remove_DTS.strip()
    Path_player = Path_player.strip()
    Preserve_menu_disc2 = Preserve_menu_disc2.strip()
    Remove_menu = Remove_menu.strip()
    Remove_PGC = Remove_PGC.strip()
    Rewind = Rewind.strip()
    Subtitle = Subtitle.strip()
    Title = Title.strip()
    Volume = Volume.strip()

    case.update(Num = Num, Num_test_link = Num_test_link, Iso_type = Iso_type, Mode = Mode, Src_iso = Src_iso, Dest_type = Dest_type, Out_disc = Out_disc, Profile = Profile, Enable_2Dto3D = Enable_2Dto3D, \
               Remove_HD_audio = Remove_HD_audio, Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1, Video_decoder_MPEG2 = Video_decoder_MPEG2, \
               Video_encoder_H264 = Video_encoder_H264, BD3D_convert_type = BD3D_convert_type, Compress_to_AC3 = Compress_to_AC3, DVDFab_description = DVDFab_description, Src_folder = Src_folder, \
               Src_path = Src_path, Audio = Audio, Audio_type = Audio_type, Change_play_order = Change_play_order, Copy_IFO = Copy_IFO, Display_forced_sub = Display_forced_sub, \
               Jump_menu = Jump_menu, Jump_main = Jump_main, Remove_DTS= Remove_DTS, Path_player = Path_player, Preserve_menu_disc2 = Preserve_menu_disc2, Remove_menu = Remove_menu, \
               Remove_PGC = Remove_PGC, Rewind = Rewind, Subtitle = Subtitle, Title = Title, Volume = Volume)
    return HttpResponseRedirect('/case/') 


def update_client_page(request):
    param1 = request.GET['index']
    client = Client.objects.get(id = param1)
    return render_to_response('update_client.html',{'client':client, 'param1':param1})


def update_client(request,param1):
    client = Client.objects.get(id = param1)
    PC_name = request.GET.get('PC_name', '')
    PC_ip = request.GET.get('PC_ip','')
    Dvdfab_path = request.GET.get('Dvdfab_path','')
    Dest_path = request.GET.get('Dest_path','')
    
    PC_name = PC_name.strip()
    PC_ip = PC_ip.strip()
    Dvdfab_path = Dvdfab_path.strip()
    Dest_path = Dest_path.strip()
   
    client.PC_name = PC_name
    client.PC_ip = PC_ip
    client.Dvdfab_path = Dvdfab_path
    client.Dest_path = Dest_path
    client.save()
    #client.update(PC_name = PC_name, PC_ip = PC_ip, Dvdfab_path = Dvdfab_path, Dest_path = Dest_path)
 
    return HttpResponseRedirect('/client/')
    
    
def update_version_page(request,param1):
    version = Versions.objects.get(id = param1)
    return render_to_response('update_version.html',locals())


def update_version(request,param1):
    version = Versions.objects.filter(id = param1)
    Version = request.GET.get('Version','')
    Create_time = request.GET.get('Create_time','')
    Description = request.GET.get('Description','')
    Notes = request.GET.get('Notes','')
    
    Version = Version.strip()
    Create_time = Create_time.strip()
    Description = Description.strip()
    Notes = Notes.strip()
    
    version.update(Version = Version, Create_time = Create_time, Description = Description, Notes = Notes)
    return HttpResponseRedirect('/version/')


def update_BD_page(request,param1):
    bd = Samples.objects.get(id = param1)
    return render_to_response('update_BD.html',locals())


def update_BD(request,param1):
    bd = Samples.objects.filter(id = param1)
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Numbers_jar = Numbers_jar.strip()
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
    bd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
            Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/bd_samples/')


def update_DVD_page(request,param1):
    dvd = DVD_samples.objects.get(id = param1)
    return render_to_response('update_DVD.html',locals())


def update_DVD(request,param1):
    dvd = DVD_samples.objects.filter(id = param1)
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
    dvd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
                 Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)

    return HttpResponseRedirect('/dvd_samples/')


def update_BD3D_page(request,param1):
    bd3d = BD3D_samples.objects.get(id = param1)
    return render_to_response('update_BD3D.html',locals())


def update_BD3D(request,param1):
    bd3d = BD3D_samples.objects.filter(id = param1)
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Numbers_jar = Numbers_jar.strip()
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
    bd3d.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, \
                Scan_type = Scan_type, Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/bd3d_samples/')

 
def update_all_BD_page(request,param1):
     bd = Samples.objects.get(id = param1)
     context= {'request':request,'bd':bd, 'param1':param1}
     return render_to_response('update_all_BD.html',context)


def update_all_DVD_page(request,param1):
     dvd = DVD_samples.objects.get(id = param1)
     context= {'request':request,'dvd':dvd,'param1':param1}
     return render_to_response('update_all_DVD.html',context)
 

def update_all_BD3D_page(request,param1):
     bd3d = BD3D_samples.objects.get(id = param1)
     context= {'request':request,'bd3d':bd3d,'param1':param1}
     return render_to_response('update_all_BD3D.html',context)
 

def update_all_BD(request,param1):
 
    bd = Samples.objects.filter(id = param1)           
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Numbers_jar = Numbers_jar.strip()
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
     
    bd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, \
              Scan_type = Scan_type, Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/all_samples/')


def update_all_DVD(request,param1):
    dvd = DVD_samples.objects.filter(id = param1)          
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
     
    dvd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard,\
               Scan_type = Scan_type, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/all_samples/')


def update_all_BD3D(request,param1):
    bd3d = BD3D_samples.objects.filter(id = param1)        
    Name = request.GET.get('Name','')
    Video_info = request.GET.get('Video_info','')
    Audio_info = request.GET.get('Audio_info','')
    File_size = request.GET.get('File_size','')
    
    Channel = request.GET.get('Channel','')
    Framerate = request.GET.get('Framerate','')
    Standard = request.GET.get('Standard','')
    Scan_type = request.GET.get('Scan_type','')
    
    Numbers_jar = request.GET.get('Numbers_jar','')
    Company = request.GET.get('Company','')
    Locations = request.GET.get('Locations','')
    Description = request.GET.get('Description','')
    Volume_label = request.GET.get('Volume_label','')
    
    Name = Name.strip()
    Video_info = Video_info.strip()
    Audio_info = Audio_info.strip()
    File_size = File_size.strip()
    
    Channel = Channel.strip()
    Framerate = Framerate.strip()
    Standard = Standard.strip()
    Scan_type = Scan_type.strip()
    
    Numbers_jar = Numbers_jar.strip()
    Company = Company.strip()
    Locations = Locations.strip()
    Description = Description.strip()
    Volume_label = Volume_label.strip()
    
     
    bd3d.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard,\
                Scan_type = Scan_type, Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/all_samples/')


def update_session_page(request,param1):
    session = Session.objects.get(id = param1)
    return render_to_response('update_session.html',locals())


def update_session(request,param1):
    session = Session.objects.filter(id = param1)
    Num = request.GET.get('Num','')
    Sub_num = request.GET.get('Sub_num','')
    Iso_type = request.GET.get('Iso_type','')
    Mode = request.GET.get('Mode','')
    Src_path = request.GET.get('Src_path','')
    Dest_path = request.GET.get('Dest_path','')
    
    PC_name = request.GET.get('PC_name','')
    Dvdfab_path = request.GET.get('Dvdfab_path','')
    Audio = request.GET.get('Audio','')
    Audio_type = request.GET.get('Audio_type','')
    
    Change_play_order = request.GET.get('Change_play_order','')
    Copy_IFO = request.GET.get('Copy_IFO','')
    Display_forced_sub = request.GET.get('Display_forced_sub','')
    Jump_menu = request.GET.get('Jump_menu','')
    
    Jump_main = request.GET.get('Jump_main','')  
    Out_disc = request.GET.get('Out_disc','')
    Path_player = request.GET.get('Path_player','')
    Preserve_menu_disc2 = request.GET.get('Preserve_menu_disc2','')
    Profile = request.GET.get('Profile','')
    
    Remove_DTS = request.GET.get('Remove_DTS','')
    Remove_HD_audio = request.GET.get('Remove_HD_audio','')
    Remove_menu = request.GET.get('Remove_menu','')
    Remove_PGC = request.GET.get('Remove_PGC','')
    
    Rewind = request.GET.get('Rewind','')
    Subtitle = request.GET.get('Subtitle','')
    Title = request.GET.get('Title','')
    Volume = request.GET.get('Volume','')
    
    Video_decoder_H264 = request.GET.get('Video_decoder_H264','')
    Video_decoder_VC1 = request.GET.get('Video_decoder_VC1','')    
    Video_decoder_MPEG2 = request.GET.get('Video_decoder_MPEG2','')
    Video_encoder_H264 = request.GET.get('Video_encoder_H264','')
    DVDFab_description = request.GET.get('DVDFab_description','')
    
    Start_time = request.GET.get('Start_time','')
    End_time = request.GET.get('End_time','')
    Total_time = request.GET.get('Total_time','')
    Flag = request.GET.get('Flag','')
    Folder_size = request.GET.get('Folder_size','')
    Init_time = request.GET.get('Init_time','')
    
    Web_log_path = request.GET.get('Web_log_path','')
    Log_folder_path = request.GET.get('Log_folder_path','')
    Result = request.GET.get('Result','')
    Developer = request.GET.get('Developer','')
    
    Enable_2Dto3D = request.GET.get('Enable_2Dto3D','')
    BD3D_convert_type = request.GET.get('BD3D_convert_type','')
    Compress_to_AC3 = request.GET.get('Compress_to_AC3','')
    Current_src_path = request.GET.get('Current_src_path','')
    #dict = {('一月').decode('GB2312'):1, ('二月').decode('GB2312'):2, ('三月').decode('GB2312'):3, ('四月').decode('GB2312'):4, ('五月').decode('GB2312'):5, ('六月').decode('GB2312'):6,\
    #        ('七月').decode('GB2312'):7, ('八月').decode('GB2312'):8, ('九月').decode('GB2312'):9, ('十月').decode('GB2312'):10, ('十一月').decode('GB2312'):11, ('十二月').decode('GB2312'):12}
    dict = [('一月').decode('GB2312'),'1', ('二月').decode('GB2312'),'2', ('三月').decode('GB2312'),'3', ('四月').decode('GB2312'),'4', ('五月').decode('GB2312'),'5', ('六月').decode('GB2312'),'6',\
            ('七月').decode('GB2312'),'7', ('八月').decode('GB2312'),'8', ('九月').decode('GB2312'),'9', ('十月').decode('GB2312'),'10', ('十一月').decode('GB2312'),'11', ('十二月').decode('GB2312'),'12']
    
    a1 = Init_time.split(' ')    
    a2 = a1[1].split(',')  
    #a1[0] == ('十一月').decode('GB2312') 
    index = dict.index(a1[0])                        #a1[0]是汉字编码
    #return HttpResponse(a1[0])
    a2.append(dict[index + 1])
   # a2.append(dict[('十一月').decode('GB2312')])
    date=a2[0]
    a2.remove(date)
    a2.append(date)
    Init_time = Start_time[0:4] + '-'.join(a2)
   
    session.update(Num = Num,  Sub_num = Sub_num, Iso_type = Iso_type, Mode = Mode, Src_path = Src_path, Dest_path = Dest_path, PC_name = PC_name, Dvdfab_path = Dvdfab_path, Audio = Audio, \
                   Audio_type = Audio_type, Change_play_order = Change_play_order, Copy_IFO = Copy_IFO,  Display_forced_sub = Display_forced_sub, Jump_menu = Jump_menu, \
                   Jump_main = Jump_main, Out_disc = Out_disc, Path_player = Path_player, Preserve_menu_disc2 = Preserve_menu_disc2, Profile = Profile, Remove_DTS = Remove_DTS,\
                   Remove_HD_audio = Remove_HD_audio, Remove_menu = Remove_menu,  Remove_PGC = Remove_PGC, Rewind = Rewind, Subtitle = Subtitle, Title = Title, Volume = Volume, \
                   Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1, Video_decoder_MPEG2 = Video_decoder_MPEG2, Video_encoder_H264 = Video_encoder_H264,\
                   DVDFab_description = DVDFab_description, Start_time = Start_time, End_time = End_time, Total_time = Total_time ,Flag = Flag, Folder_size = Folder_size, \
                   Init_time = Init_time, Web_log_path = Web_log_path,  Log_folder_path = Log_folder_path, Result = Result,Developer = Developer, Enable_2Dto3D = Enable_2Dto3D,\
                   BD3D_convert_type = BD3D_convert_type, Compress_to_AC3 = Compress_to_AC3, Current_src_path = Current_src_path)
    
    return HttpResponseRedirect('/session/')


def update_test_result_page(request,param1): 
    session = Session.objects.get(id = param1) 
    if '\\' in session.Src_path:
        src_iso = session.Src_path.split('\\')[-1]
        src_path = session.Src_path.replace('\\' + src_iso, '')    
    else:
        src_iso = session.Src_path.split('/')[-1]
        src_path = session.Src_path.replace('/' + src_iso, '')
         
    #if session.Mode.upper().startswith('DVD') or session.Mode.upper().startswith('FULLDISC'):
    if session.Iso_type.upper() == 'DVD':
        try:   
            iso = dvd = DVD_samples.objects.filter(Name = src_iso)
        except Exception, e:
            print str(e)
    
    #elif session.Mode.upper().startswith('BD') or session.Mode.upper().startswith('BLURAY') and '3D' not in src_iso.upper():    
    elif session.Iso_type.upper() == 'BD':    
        try:
            iso = bd = Samples.objects.filter(Name = src_iso)
        except Exception, e:
            print str(e)
            
    elif '3D' in src_iso.upper():
        try:
            iso = bd3d = BD3D_samples.objects.filter(Name = src_iso)
        except Exception, e:
            print str(e)
    else:
        iso = video = ''
        pass
    
    return render_to_response('update_test_result.html',locals())


def update_test_result(request,param1):   
    session = Session.objects.filter(id = param1)  
    Num = request.GET.get('Num','')
    Sub_num = request.GET.get('Sub_num','')
    Iso_type = request.GET.get('Iso_type','')
    Mode = request.GET.get('Mode','')
    Src_path = request.GET.get('Src_path','')
    
    Dest_path = request.GET.get('Dest_path','')
    PC_name = request.GET.get('PC_name','')
    Dvdfab_path = request.GET.get('Dvdfab_path','')
    Audio = request.GET.get('Audio','')
    
    Audio_type = request.GET.get('Audio_type','')
    Change_play_order = request.GET.get('Change_play_order','')
    Copy_IFO = request.GET.get('Copy_IFO','')
    Display_forced_sub = request.GET.get('Display_forced_sub','')
    
    Jump_menu = request.GET.get('Jump_menu','')
    Jump_main = request.GET.get('Jump_main','')
    Out_disc = request.GET.get('Out_disc','')
    Path_player = request.GET.get('Path_player','')
    
    Preserve_menu_disc2 = request.GET.get('Preserve_menu_disc2','')
    Profile = request.GET.get('Profile','')
    Remove_DTS = request.GET.get('Remove_DTS','')
    Remove_HD_audio = request.GET.get('Remove_HD_audio','')
    Remove_menu = request.GET.get('Remove_menu','')
    Remove_PGC = request.GET.get('Remove_PGC','')
    
    Rewind = request.GET.get('Rewind','')
    Subtitle = request.GET.get('Subtitle','')
    Title = request.GET.get('Title','')
    Volume = request.GET.get('Volume','')
    
    Video_decoder_H264 = request.GET.get('Video_decoder_H264','')
    Video_decoder_VC1 = request.GET.get('Video_decoder_VC1','')    
    Video_decoder_MPEG2 = request.GET.get('Video_decoder_MPEG2','')
    Video_encoder_H264 = request.GET.get('Video_encoder_H264','')
    DVDFab_description = request.GET.get('DVDFab_description','')
      
    Start_time = request.GET.get('Start_time','')
    End_time = request.GET.get('End_time','')
    Total_time = request.GET.get('Total_time','')
    Flag = request.GET.get('Flag','')
    Folder_size = request.GET.get('Folder_size','')
    Init_time = request.GET.get('Init_time','')
    #dict = {'一月':'1', '二月':'2', '三月':'3', '四月':'4', '五月':'5', '六月':'6', '七月':'7', '八月':'8', '九月':'9', '十月':'10', '十一月':'11', '十二月':'12'}
    dict = [('一月').decode('GB2312'),'1', ('二月').decode('GB2312'),'2', ('三月').decode('GB2312'),'3', ('四月').decode('GB2312'),'4', ('五月').decode('GB2312'),'5', ('六月').decode('GB2312'),'6',\
            ('七月').decode('GB2312'),'7', ('八月').decode('GB2312'),'8', ('九月').decode('GB2312'),'9', ('十月').decode('GB2312'),'10', ('十一月').decode('GB2312'),'11', ('十二月').decode('GB2312'),'12']
    a1 = Init_time.split(' ')
    a2 = a1[1].split(',')
    #a1[0] == ('十一月').decode('GB2312')
    index = dict.index(a1[0])                      #a1[0]是汉字编码
   # return HttpResponse(a1[0])
    a2.append(dict[index + 1])
    date=a2[0]
    a2.remove(date)
    a2.append(date)
    current_year = time.strftime("%Y-%m-%d %H:%M:%S")[0:4]
    Init_time = current_year + '-'.join(a2)
   
    Web_log_path = request.GET.get('Web_log_path','')
    Log_folder_path = request.GET.get('Log_folder_path','')
    Result = request.GET.get('Result','')
    Developer = request.GET.get('Developer','')
    
    Enable_2Dto3D = request.GET.get('Enable_2Dto3D','')
    BD3D_convert_type = request.GET.get('BD3D_convert_type','')
    Compress_to_AC3 = request.GET.get('Compress_to_AC3','')
    Current_src_path = request.GET.get('Current_src_path','')
    
    session.update(Num = Num, Sub_num = Sub_num, Iso_type = Iso_type, Mode = Mode, Src_path = Src_path, Dest_path = Dest_path, PC_name = PC_name, Dvdfab_path = Dvdfab_path, Audio = Audio,\
                   Audio_type = Audio_type, Change_play_order = Change_play_order, Copy_IFO = Copy_IFO,  Display_forced_sub = Display_forced_sub, Jump_menu = Jump_menu,\
                   Jump_main = Jump_main, Out_disc = Out_disc, Path_player = Path_player, Preserve_menu_disc2 = Preserve_menu_disc2, Profile = Profile, Remove_DTS = Remove_DTS,\
                   Remove_HD_audio = Remove_HD_audio, Remove_menu = Remove_menu,  Remove_PGC = Remove_PGC, Rewind = Rewind, Subtitle = Subtitle, Title = Title, Volume = Volume, \
                   Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1, Video_decoder_MPEG2 = Video_decoder_MPEG2, Video_encoder_H264 = Video_encoder_H264,\
                   DVDFab_description = DVDFab_description, Start_time = Start_time, End_time = End_time, Total_time = Total_time ,Flag = Flag, Folder_size = Folder_size,\
                   Init_time = Init_time, Web_log_path = Web_log_path, Log_folder_path = Log_folder_path, Result = Result, Developer = Developer, Enable_2Dto3D = Enable_2Dto3D,\
                   BD3D_convert_type = BD3D_convert_type, Compress_to_AC3 = Compress_to_AC3, Current_src_path = Current_src_path)
    
    return HttpResponseRedirect('/test_result/')


def display_bdverify_log(request):
    return render_to_response('error.html')


def display_log(request, param1):
    session = Session.objects.get(id = param1)
    log_path = 'd:/DVDfab_log'
    try:
        list_log = os.listdir(log_path)
        for log in list_log:    
            if str(session.id) + '_' + 'dvdfab_internal.log' == log:
        #if 'internal_log' == log.replace('_' + log.split('_')[-1], '') and str(session.id) == str(log.split('_')[-1]):
                file_content = file(log_path + '/' + log, 'r')
                contexts = file_content.readlines()
                break    
        return render_to_response('display_log.html',{'contexts':contexts})
    except Exception, e:
        return render_to_response('error.html')


@csrf_exempt
def upload_file(request, param1):
  if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
          #return HttpResponse(request.TITLES["title"])
          destination = open('d:/DVDfab_log/' + request.FILES["file"].name, 'wb+')
          for chunk in request.FILES['file'].chunks():
              destination.write(chunk)
          destination.close()
          return HttpResponseRedirect('/update_test_result_page/' + param1)   
      else:
          return HttpResponseRedirect('/update_test_result_page/' + param1)     
  else:
     form = UploadFileForm()
     return HttpResponseRedirect('/update_test_result_page/' + param1)

'''
def handle_uploaded_file(f):
  destination = open('d:/wenjian/file.txt', 'a+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()
'''

def download_test_zipfile(request):
    temp = tempfile.TemporaryFile() 
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    src = "d:/develop/dvdfab_auto_test_scripts/dist/"   
    files = os.listdir(src) 
    for filename in files:   
        archive.write(src+'/'+filename, filename)
    archive.close() 
    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=dvdfab_test_scripts.zip' 
    response['Content-Length'] = temp.tell()  
    temp.seek(0) 
    return response


def download_test_zipfile_for_mac(request):
    temp = tempfile.TemporaryFile() 
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    src = "d:/develop/dvdfab_auto_test_scripts/dvdfab_auto_test_scripts_mac/"   
    files = os.listdir(src) 
    for filename in files:   
        archive.write(src+'/'+filename, filename)
    archive.close() 
    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=dvdfab_test_scripts_mac.zip' 
    response['Content-Length'] = temp.tell()  
    temp.seek(0) 
    return response



def download_log_folder(request, param1):
    src = "d:/DVDFab_log" 
    if not os.path.exists(src):
        os.mkdir(src)
    temp = tempfile.TemporaryFile() 
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    try:
        files = os.listdir(src) 
    except:
        return render_to_response('error.html')
    #for filename in files:   
    if param1 + '_dvdfab_internal.log' in files:
        archive.write(src+'/' + param1 + '_dvdfab_internal.log', param1 + '_dvdfab_internal.log')
    else:
        return render_to_response('error.html')
    archive.close() 
    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename = dvdfab_log_folder.zip' 
    response['Content-Length'] = temp.tell()  
    temp.seek(0) 
    return response












