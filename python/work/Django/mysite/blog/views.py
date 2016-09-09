#-*- coding:utf-8 -*-
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.db.models import Q
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator,InvalidPage, EmptyPage,PageNotAnInteger

import string
import time
import datetime
import os
import subprocess
import tempfile, zipfile 

from mysite import settings
from forms import * 
from models import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


@csrf_exempt
def index(request):
    import getpass
    user = getpass.getuser()
    return render_to_response('base.html',{"user":user})


def about(request, template, extra_context):
    return HttpResponse(extra_context["xdd"])
    try:
        return direct_to_template(request, template)
    except TemplateDoesNotExist:
        raise Http404()

def object_list(request, model, template_name):
    obj_list = model.objects.all()
    return render_to_response(template_name, {"obj_list": obj_list})

"""
def client(request):
    #client = Client.objects.all()
    #client = Client.objects.all().values()[1]
    ziduan = request.GET.get("ziduan","").strip()
    desc = request.GET.get("desc","").strip()
    if ziduan == "id":
        if desc == "1" or desc == "":
            client = Client.objects.all().order_by(ziduan)
            desc = 2
        elif desc == "2":
            client = Client.objects.all().order_by("-" + ziduan)
            desc = 1
        else:
            desc = 1
            client = Client.objects.all()
    elif ziduan == "PC_name":
        if desc == "1" or desc == "":
            client = Client.objects.all().order_by(ziduan)
            desc = 2
        elif desc == "2":
            client = Client.objects.all().order_by("-" + ziduan)
            desc = 1
        else:
            desc = 1
            client = Client.objects.all()
    else:
        client = Client.objects.all()

    return render_to_response('client.html', locals())
"""

#用分页类分页显示
@login_required
def test(request):
    sessions = Session.objects.all()
    after_range_num = 5      #当前页面之前显示5页
    befor_range_num = 4      #当前页面之后显示4页
    #如果请求的页码少于1或者类型错误，则跳转至第1页
    try:              
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    ziduan = request.GET.get("ziduan","").strip()
    sort = request.GET.get("sort","").strip()
          
    paginator = Paginator(sessions,10)   #设置session在每页显示的数量，这里为10

    #跳转至请求页面，如果该页不存在或者超过则跳转到尾页
    try:
        session_list = paginator.page(page)     
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        page = paginator.num_pages
        session_list = paginator.page(page)
        
    # 1 and "" 代表降序， 2代表升序    
    record_list = ["index", "Num"] 
    for record in record_list: 
        if ziduan == record:
            #降序
            if sort == "1":
                #session_list不是一个list，而是一个类的对象
                session_list = paginator.page(page)
                session_list_new = session_list
                sort = "2"
            #升序
            elif sort == "2":
                session_list = paginator.page(page)
                #经过切片之后，才是一个list，session_list.object_list也是一个list
                session_list_new = session_list[::-1]
                sort = "1"
            else:
                session_list = paginator.page(page)
                session_list_new = session_list
                sort = "2"
            break
    if ziduan not in record_list:
        session_list = paginator.page(page)
        session_list_new = session_list
        #sort = "2"

    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num : page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return render_to_response("test.html",locals())


def fenye(request):
    sessions = Session.objects.all()
    after_range_num = 5
    befor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
    except ValueError:
        page = 1
    paginator = Paginator(sessions,50)

    #跳转至请求页面，如果该页不存在或者超过则跳转至尾页
    try:
        session_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        page = paginator.num_pages
        session_list = paginator.page(paginator.num_pages)
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num: page + befor_range_num]
    else:
        page_range = paginator.page_range[0: page + befor_range_num]
    return render_to_response("test.html",locals())
    

@csrf_exempt
def register(request):
    #return HttpResponse(settings.BASE_DIR)
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username","").strip()
            password = request.POST.get("password","").strip()
            email = request.POST.get("email","").strip()
            user = User.objects.create_user(username,email,password)
            user.save()
            request.session["username"] = username
            return HttpResponseRedirect("/test/")
    else:
        form = UserForm()
    return render_to_response("register.html",locals())


@csrf_exempt
def login(request,template_name=''):
    if request.session.has_key("username"):
        return HttpResponseRedirect("/test/")
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        password = request.POST.get("password","").strip()
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session["username"] = username
            return HttpResponseRedirect("/test/")
        else:
            return HttpResponse("<a href = ''>请重新登陆</a>")
    return render_to_response("login.html", locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")


def get_check_code_image(request,image = "media/checkcode.gif"):
    import Image, ImageDraw, ImageFont,random
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    mp = md5.new()
    mp_src = mp.update(str(datetime.now()))
    mp_src = mp.hexdigest()
    rand_str = mp_src[0:4]
    draw.text((10,10),rand_str[0],font = ImageFont.truetype("ARIAL.TTF",random.randrange(25,50)))
    draw.text((48,10),rand_str[1],font = ImageFont.truetype("ARIAL.TTF",random.randrange(25,50)))
    draw.text((85,10),rand_str[2],font = ImageFont.truetype("ARIAL.TTF",random.randrange(25,50)))
    draw.text((120,10),rand_str[3],font = ImageFont.truetype("ARIAL.TTF",random.randrange(25,50)))
    del draw
    reuqest.session["checkcode"] = rand_str
    buf = cStringIO.StringIO()
    im.save(buf,"gif")
    return HttpResponse(buf.getvalue(),"image/gif")


def new_add_case(request):
    if request.method == "POST":
        Num = request.POST.get('Num','').strip()
        Num_test_link = request.POST.get('Num_test_link','').strip()
        Iso_type = request.POST.get('Iso_type','').strip()
        Mode = request.POST.get('Mode','').strip()
        Src_iso = request.POST.get('Src_iso','').strip()
        Dest_type = request.POST.get('Dest_type','').strip()
        Out_disc = request.POST.get('Out_disc','').strip()
        Profile = request.POST.get('Profile','').strip()
        Enable_2Dto3D = request.POST.get('Enable_2Dto3D','').strip()
        Remove_HD_audio = request.POST.get('Remove_HD_audio','').strip()
        
        Video_decoder_H264 = request.POST.get('Video_decoder_H264','').strip()
        Video_decoder_VC1 = request.POST.get('Video_decoder_VC1','').strip()
        Video_decoder_MPEG2 = request.POST.get('Video_decoder_MPEG2','').strip()
        Video_encoder_H264 = request.POST.get('Video_encoder_H264','').strip()
        BD3D_convert_type = request.POST.get('BD3D_convert_type','').strip()
        Compress_to_AC3 = request.POST.get('Compress_to_AC3','').strip()
        DVDFab_description = request.POST.get('DVDFab_description','').strip()
        Src_folder = request.POST.get('Src_folder','').strip()
        Src_path = request.POST.get('Src_path','').strip()
        
        Audio = request.POST.get('Audio','').strip()
        Audio_type = request.POST.get('Audio_type','').strip()
        Change_play_order = request.POST.get('Change_play_order','').strip()
        Copy_IFO = request.POST.get('Copy_IFO','').strip()
        Display_forced_sub = request.POST.get('Display_forced_sub','').strip()
        Jump_menu = request.POST.get('Jump_menu','').strip()
        Jump_main = request.POST.get('Jump_main','').strip()
        Remove_DTS = request.POST.get('Remove_DTS','').strip()
        Path_player = request.POST.get('Path_player','').strip()
        Preserve_menu_disc2 = request.POST.get('Preserve_menu_disc2','').strip()
        Remove_menu = request.POST.get('Remove_menu','').strip()
        Remove_PGC = request.POST.get('Remove_PGC','').strip()
        Rewind = request.POST.get('Rewind','').strip()
        Subtitle = request.POST.get('Subtitle','').strip()
        Title = request.POST.get('Title','').strip()
        Volume = request.POST.get('Volume','').strip()
        
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
     context = {}
     if request.method == "POST":
         PC_name = request.POST.get('PC_name','').strip()
         PC_ip = request.POST.get('PC_ip','').strip()
         Dvdfab_path = request.POST.get('Dvdfab_path','').strip()
         Dest_path = request.POST.get('Dest_path','').strip()
         
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
             #last_id = Client.objects.latest("id").id
             return HttpResponseRedirect('/client/')
     return render_to_response('new_client.html',context,context_instance=RequestContext(request))


def new_add_obj(request, template_name, model, url, numbers_jar_flag):
    if request.method == "POST":
        Name = request.POST.get('Name','').strip()
        Video_info = request.POST.get('Video_info','').strip()
        Audio_info = request.POST.get('Audio_info','').strip()
        File_size = request.POST.get('File_size','').strip()
        Channel = request.POST.get('Channel','').strip()
        Framerate = request.POST.get('Framerate','').strip()
        Standard = request.POST.get('Standard','').strip()
        Scan_type = request.POST.get('Scan_type','').strip()
        Numbers_jar = request.POST.get('Numbers_jar','').strip()
        Company = request.POST.get('Company','').strip()
        Locations = request.POST.get('Locations','').strip()
        Description = request.POST.get('Description','').strip()
        Volume_label = request.POST.get('Volume_label','').strip()
        if numbers_jar_flag: 
            obj = model(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
                    Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
        else:
            obj = model(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
                    Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
        
        if Name:
            obj.save()
            return HttpResponseRedirect(url)
    return render_to_response(template_name)


def new_add_version(request):
    if request.method == "POST":
        Version = request.POST.get('Version','').strip()
        Create_time = request.POST.get('Create_time','').strip()
        Description = request.POST.get('Description','').strip()
        Notes = request.POST.get('Notes','').strip()
        
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
    return render_to_response('new_version.html')#,context, context_instance=RequestContext(request))


def case(request):
    case_type = request.GET.get('case_type','')
    client = Client.objects.all().order_by("PC_name")
    version = Versions.objects.all()[0:3]
    
    #Blu_Copy
    if case_type == 'Blu_Copy':   
        qs = Case.objects.filter(Q(Mode__iexact = 'fulldisc') | Q(Mode__iexact = 'mainmovie')).order_by('Num') 
        case = qs.filter(Q(Iso_type__iexact = 'BD')).order_by("Num")   
    elif case_type == 'BC_P0_2':
        case = Case.objects.filter(Num__gte = '026').order_by('Num').filter(Num__lte = '050')
        
    elif case_type == 'BC_P1_1':
        case = Case.objects.filter(Num__gte = '051').order_by('Num').filter(Num__lte = '076')
    elif case_type == "BC_P1_2":
        case = Case.objects.filter(Q(Mode = "bdfulldisc") | Q(Mode = "bdmainmovie")).order_by("Num").filter(Num__gte = "101").filter(Num__lte = "125")
    elif case_type == 'BC_P1_3':
        case = Case.objects.filter(Num__gte = '701').order_by('Num').filter(Num__lte = '730')
    elif case_type == 'BC_P2':
        case = Case.objects.filter(Num__gte = "151").order_by("Num").filter(Num__lte = "175")
    elif case_type == 'BC_P3':
        case = Case.objects.filter(Num__gte = "176").order_by("Num").filter(Num__lte = "200")
    
    #Blu_ Ripper    
    elif case_type == 'Blu_Ripper':
        case = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num") 
        #case = qs.exclude(Q(Mode__icontains = "dvd") | Q(Mode__icontains = "3d")).order_by("Num")      
    elif case_type == "BR_P0":
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num")
        case = qs.filter(Num__gte = "201").order_by("Num").filter(Num__lte = "290")       
    elif case_type == "BR_P1":
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num")
        case = qs.filter(Num__gte = "291").order_by("Num").filter(Num__lte = "380")    
    elif case_type == "BR_P2":
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type__iexact = "BD")).order_by("Num")
        case = qs.filter(Num__gte = "381").order_by("Num").filter(Num__lte = "400")   
    
    #DVD_Copy        
    elif case_type == 'DVD_Copy':
        qs = Case.objects.filter(Q(Mode__iexact = "fulldisc") | Q(Mode__iexact = "mainmovie")).order_by("Num")
        case = qs.filter(Q(Iso_type__iexact = 'DVD')).order_by("Num")
    elif case_type == 'DC_P0':
        case = Case.objects.filter(Num__gte = "601").order_by("Num").filter(Num__lte = "620")

    #DVD_Ripper        
    elif case_type == 'DVD_Ripper':
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type = "DVD")).order_by("Num")
        case = qs.filter(Q(Num__gte = "401") & Q(Num__lte = "600")).order_by("Num")    
    elif case_type == 'DR_P0':
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type = "DVD")).order_by("Num")
        case = qs.filter(Num__gte = "401").order_by("Num").filter(Num__lte = "500")
    elif case_type == 'DR_P1':
        qs = Case.objects.filter(Q(Mode__icontains = "Ripper") & Q(Iso_type = "DVD")).order_by("Num")
        case = qs.filter(Num__gte = "501").order_by("Num").filter(Num__lte = "600")
   
    #Blu_DVD
    elif case_type == 'Blu_DVD':
        cae = Case.objects.filter(Q(Mode__iexact = "bluraydvd")).order_by("Num")
        case = Case.objects.filter(Q(Num__gte = "801") & Q(Num__lte = "824")).order_by("Num") 
    elif case_type == 'BD_P0':
        case = Case.objects.filter(Num__gte = "801").order_by("Num").filter(Num__lte = "824")    
    #Blu_3D        
    elif case_type == 'Blu_3D':
        case = Case.objects.filter(Q(Mode__icontains = "bluray3d")).order_by("Num")  
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
        case = qs.filter(Num__gte = "1000").filter(Num__lte = "1100")     

    #2Dto3D
    elif case_type == '2Dto3D':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        case = qs.filter(Num__gte = "1101").filter(Num__lte = "1399")          
    elif case_type == '2T3_DR':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        case = qs.filter(Num__gte = "1101").filter(Num__lte = "1199")     
    elif case_type == '2T3_BR':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        case = qs.filter(Num__gte = "1201").filter(Num__lte = "1299")
    elif case_type == '2T3_VC':
        qs = Case.objects.filter(Q(Enable_2Dto3D__icontains = "yes")).order_by("Num")
        case = qs.filter(Num__gte = "1301").filter(Num__lte = "1399")
    
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
        case = qs.filter(Q(Num__gte = "4012") & Q(Num__lte = "4029"))
        
    #DVDCreator
    elif case_type == 'DVDCreator':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        case = qs.filter(Q(Num__gte = "4000") & Q(Num__lte = "4011"))

    elif case_type == 'DVD_DVD5':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        case = qs.filter(Num__gte = "4000").filter(Num__lte = "4005")     
    elif case_type == 'DVD_DVD9':
        qs = Case.objects.filter(Q(Mode__iexact = "creator")).order_by("Num")
        case = qs.filter(Num__gte = "4006").filter(Num__lte = "4011")
               
    else:
        qs = Case.objects.filter(Num__gte = "001").order_by("Num")
        case = qs.filter(Num__lte = "025")
    return render_to_response('case.html', locals())


def get_src_path(Iso_type, case):
    if Iso_type.upper() == 'BD':
        Src_path = '/U_nas/volume1/bd/' + case.Src_iso
    elif Iso_type.upper() == 'DVD':
        Src_path = '/U_nas/volume2/dvd/' + case.Src_iso
    else:
        Src_path = '/U_nas/volume3/video/' + case.Src_iso
    return Src_path


@csrf_exempt  
def insert_session(request):  
        checkbox = request.POST.getlist('checkbox')
        pc_name_list = request.POST.getlist('pc_name')
        dvdfab_path_list = request.POST.getlist('dvdfab_path')
        num_list = request.POST.getlist('num')
        select_version_list = request.POST.getlist('select_version')
        Start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        start_time = Start_time.replace('-','_').replace(":", "_")
        path = start_time.replace(' ','_')
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
            Src_path = get_src_path(Iso_type, case)
            Start_time = time.strftime('%Y-%m-%d %H:%M:%S')
            DVDFab_description = case.DVDFab_description
            Flag = 0
            Sub_num = End_time = Total_time = Web_log_path = Log_folder_path = Dvdfab_path = Current_src_path = Folder_size = Result = Developer = Dest_path = ''
            
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
                name = str(session.id) + '_'+ path  + '_' + num + '/' + case.Src_iso
            else: 
                name = str(session.id) + '_'+ path  + '_' + num
            Dest_path = os.path.join(client_dest_path, name)
            session.Dest_path = Dest_path
            session.save()
        return  HttpResponseRedirect('/case/') 
                


def client(request):
    ziduan = request.GET.get("ziduan","").strip()
    desc = request.GET.get("desc","").strip()
    client = Client.objects.all()
    record_list = ["id", "PC_name", "PC_ip", "Dvdfab_path", "Dest_path"]
    for record in record_list:
        if ziduan == record:
            if desc == "1" or desc == "":
                client = Client.objects.all().order_by(ziduan)
                desc = 2
            elif desc == "2":
                client = Client.objects.all().order_by("-" + ziduan)
                desc = 1
            else:
                desc = 1
                client = Client.objects.all()
    return render_to_response('client.html', locals())


def version(request): 
    obj_list = Versions.objects.all()
    return render_to_response('version.html', locals())


def all_samples(request):  
    bd_samples = Samples.objects.all()
    dvd_samples = DVD_samples.objects.all()
    bd3d_samples = BD3D_samples.objects.all()
    return render_to_response('all.html', locals())


def session(request):
    per_page_count = 50 
    nowpage = request.GET.get('nowpage','')
    ziduan = request.GET.get("ziduan","").strip()
    sort = request.GET.get("sort","").strip()
    if nowpage == '':
        nowpage = 1
    else:
        nowpage = int(nowpage)
    count = Session.objects.count()
    if count % per_page_count == 0:
        pageall = count / per_page_count
    else:
        pageall = count / per_page_count + 1
    if nowpage - 1 < 1:
        pageup = 1
    else:
        pageup = nowpage - 1
    if nowpage + 1 >= pageall:
        pagedn = pageall
    else:
        pagedn = nowpage + 1
    start = per_page_count * (nowpage - 1)
    if ziduan == "index":
        if sort == "1" or sort == "":
            sort = "2"
            session = Session.objects.all().order_by('-id')[start:(start + per_page_count)]
        elif sort == "2":
            sort = "1"
            session = Session.objects.all().order_by('-id')[start:(start + per_page_count)][::-1]
    else:
        session = Session.objects.all().order_by('-id')[start:(start + per_page_count)]
    return render_to_response('session.html', locals())

 
def search_session(request):
    api = request.GET.get('api','').strip()         #index, Mode, PC_name, Num, Result ....
    api_name = request.GET.get('api_name','').strip()
    sample_name = request.GET.get('sample_name','').strip()
    if api_name:
        record_list = ["id", "Mode", "Src_path", "Num", "Result", "Out_dics", "PC_name", "Profile", "Developer"]
        for each_record in record_list:
            if api == each_record:
                search_str = "%s like '%%%%%s%%%%'" % (each_record, str(api_name))
                #search_str = "Name like '%%" + str(all_type) + "%%'"
                session = Session.objects.extra(where = [search_str])
                if not session:
                    return render_to_response('error.html')
                else:
                    break
        return render_to_response('session.html',locals()) 
    else:
        return HttpResponseRedirect('/session/')
 
def search_object(request, template_name, model):
    obj_list = model.objects.all()
    return render_to_response(template_name, locals()) 


@csrf_exempt
def test_result(request):
    day_info_list = []
    PC_name = check_Flag = ""
    ziduan = request.GET.get('ziduan','').strip()
    client = Client.objects.all().order_by('PC_name') 
    try:        
        web_params = Web_params.objects.all()[0] 
        days = int(web_params.Days_display)
    except:
        days = 7
    now_day = datetime.datetime.now()
    for day in range(days):
        record_list = ["Index", "Num", "Mode","PC_name","Out_disc","Remove_HD_audio","BD3D_convert_type","Compress_to_AC3",\
                       "Video_decoder_H264","Video_decoder_VC1","Video_decoder_MPEG2","Video_encoder_H264","Enable_2Dto3D",\
                       "Profile","Src_path","Dest_path","Start_time","End_time","Total_time","Folder_size","DVDFab_description",\
                       "Result","Developer","Flag"]
        for record in record_list:
            if ziduan == record:
                if ziduan == "Index":
                    ziduan = "id"
                session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day)).order_by('%s'% ziduan)
                break
            else:
                session = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day))
        session1 = session.filter(PC_name = PC_name) if PC_name else session 
        session2 = session1.filter(Flag = check_Flag) if check_Flag else session1
        if session2:
            day_info_list.append([session[0].Init_time,session2])
    if request.method == "POST":
        list = []
        list_str_int = []
        days_info_list = []
        PC_name = request.POST.get('PC_name', '').strip()
        check_Flag = request.POST.get('check_Flag', '').strip()
        test_api = request.POST.get('test_api','').strip()
        test_name = request.POST.get('test_name','').strip()
        Flag = request.POST.get('Flag','').strip()
        Flag_old = request.POST.get('Flag_old','').strip()
        update_flag_from_day = request.POST.get('update_flag_from_day','').strip()
        update_flag_to_day = request.POST.get('update_flag_to_day','').strip()
        PC_name_by_day = request.POST.get('PC_name_by_day', '').strip()
        Flag_old_by_day = request.POST.get('Flag_old_by_day','').strip()
        Flag_by_day = request.POST.get('Flag_by_day','').strip()
        update_flag_from_day = update_flag_from_day.replace('/','-').replace(".","-").replace(",","-")
        update_flag_to_day = update_flag_to_day.replace('/','-').replace(".","-").replace(",","-")
        days = request.POST.get('days','').strip()
        #return HttpResponse("%s-%s"%(Flag_old_by_day, Flag_by_day))
        try:
            days = int(days)      
            if days != 0:
                web = Web_params(Days_display = days)   
                web.save()
        except Exception:
            pass     
            
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
                session = qs.filter(Flag = Flag_old) if Flag_old else qs
                if Flag:
                    session.update(Flag = Flag)        
        elif test_api == 'PC_name' and test_name:      
            test_name = test_name.split(',')
            for i in test_name:
                qs = Session.objects.filter(PC_name = i)    
                session = qs.filter(Flag = Flag_old) if Flag_old else qs
                if Flag:
                    session.update(Flag = Flag)        
        elif test_api == 'Init_time' and test_name:      
            test_name = test_name.replace('/','-').replace(".","-").replace(",","-")
            qs = Session.objects.filter(Init_time = test_name)  
            session = qs.filter(Flag = Flag_old) if Flag_old else qs
            if Flag:
                session.update(Flag = Flag)  
        elif test_api == 'Flag_1':
            session = Session.objects.filter(Flag = Flag_old) if Flag_old else Session.objects.all()
            if Flag:
                session.update(Flag = Flag)
        if PC_name_by_day: 
            qs = Session.objects.filter(Init_time__gte = update_flag_from_day) if update_flag_from_day else Session.objects.all()
            qs0 = qs.filter(Init_time__lte = update_flag_to_day) if update_flag_to_day else qs
            qs1 = qs0.filter(PC_name = PC_name_by_day)
            session = qs1.filter(Flag = Flag_old_by_day) if Flag_old_by_day else qs1
            if Flag_by_day:
                session.update(Flag = Flag_by_day)
        #else:
        #    return HttpResponse("Please select PC name!!")
        return HttpResponseRedirect("/test_result/")
    
    return render_to_response('test_result.html',locals())
 
    
def search_test_result(request):  
    day_info_list = []
    days_info_list = []

    test_api = request.GET.get('test_api','').strip()
    test_name = request.GET.get('test_name','').strip()
    Flag = request.GET.get('Flag','').strip()
    days = request.GET.get('days','').strip()
     
    days = int(days) if days else 7
    now_day = datetime.datetime.now()
    display_days = now_day - datetime.timedelta( days = days)
    for day in range(days):
        session1 = Session.objects.filter(Init_time = now_day - datetime.timedelta(days = day))
        if session1:
            day_info_list.append([session1[0].Init_time,session1])
    
    if test_name:
        record_list = ["id", "PC_name", "Init_time"]
        for each_record in record_list:
            if search_type == each_record:
                search_str = "%s like '%%%%%s%%%%'" % (each_record, str(test_name))
                session = Session.objects.extra(where = [search_str])
                if Flag:
                    session.update(Flag = Flag)
                if not session:
                    return render_to_response('error.html')
                break
    return render_to_response('search_test_result.html',locals())
    

@csrf_exempt
def search_type(request):
    client = Client.objects.all()
    version = Versions.objects.all()[0:3]
    search_type = request.POST.get('search_type','')
    type_context = request.POST.get('type_context','').strip()
    
    if type_context:
        record_list = ["Mode", "Src_iso", "Out_disc", "Profile"]
        for each_record in record_list:
            if search_type == each_record:
                search_str = "%s like '%%%%%s%%%%'" % (each_record, str(type_context))
                case = Case.objects.extra(where = [search_str])
                if not case:
                    return render_to_response('error.html')
                else:
                    break
        return render_to_response('case.html',locals(),context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/case/')
   
 
def search_object_type(request, template_name, model, url):
    BD = request.GET.get('category').strip()
    BD_type = request.GET.get('category_type','').strip()
    if BD_type:
        record_list = ["Name", "Locations", "Video_info", "Audio_info", "Channel", "Framerate", "Standard", "Scan_type", "Numbers_jar", "Company"]
        for each_record in record_list:
            if BD == each_record:
                search_str = "%s like '%%%%%s%%%%'" % (each_record, str(BD_type))
                obj_list = model.objects.extra(where = [search_str])
                if not obj_list:
                    return render_to_response('error.html')
                else:
                    break
        return render_to_response(template_name,locals()) 
    else:
        return HttpResponseRedirect(url)
 
def object_sort(request, template_name, model):
    return HttpResponse(template_name)
    sort_name = request.GET.get('sort_name','').strip()
    obj_list = model.objects.all().order_by(sort_name) 
    return render_to_response(template_name, locals())


def search_all_type(request):
    bd = Samples.objects.all() 
    dvd = DVD_samples.objects.all()
    bd3d = BD3D_samples.objects.all()
    All = request.GET.get('All','').strip()
    all_type = request.GET.get('all_type','').strip()
    
    if all_type:
        record_list = ["Name", "Locations", "Video_info", "Audio_info", "Channel", "Framerate", "Standard", "Scan_type", "Numbers_jar", "Company"]
        for each_record in record_list:
            if All == each_record:
                search_str = "%s like '%%%%%s%%%%'" % (each_record, str(all_type))
                #search_str = "Name like '%%" + str(all_type) + "%%'"
                bd = Samples.objects.extra(where = [search_str]) 
                dvd = DVD_samples.objects.extra(where = [search_str])
                bd3d = BD3D_samples.objects.extra(where = [search_str])
                if not bd and not dvd and not bd3d:
                    return render_to_response('error.html')
                else:
                    break
        return render_to_response('search_all_type.html',locals()) 
    else:
        return HttpResponseRedirect('/all_samples/')
            
   
def update_case(request,param1):  
    if request.method == "POST": 
        case = Case.objects.filter(id = param1)
        Num = request.POST.get('Num','').strip()
        Num_test_link = request.POST.get('Num_test_link','').strip()
        Iso_type = request.POST.get('Iso_type','').strip()
        Mode = request.POST.get('Mode','').strip()
        Src_iso = request.POST.get('Src_iso','').strip()
        Dest_type = request.POST.get('Dest_type','').strip()
        Out_disc = request.POST.get('Out_disc','').strip()
        Profile = request.POST.get('Profile','').strip()
        Enable_2Dto3D = request.POST.get('Enable_2Dto3D','').strip()
        Remove_HD_audio = request.POST.get('Remove_HD_audio','').strip()
    
        Video_decoder_H264 = request.POST.get('Video_decoder_H264','').strip()
        Video_decoder_VC1 = request.POST.get('Video_decoder_VC1','').strip()
        Video_decoder_MPEG2 = request.POST.get('Video_decoder_MPEG2','').strip()
        Video_encoder_H264 = request.POST.get('Video_encoder_H264','').strip()
        BD3D_convert_type = request.POST.get('BD3D_convert_type','').strip()
        Compress_to_AC3 = request.POST.get('Compress_to_AC3','').strip()
        DVDFab_description = request.POST.get('DVDFab_description','').strip()
        Src_folder = request.POST.get('Src_folder','').strip()
        Src_path = request.POST.get('Src_path','').strip()
    
    	Audio = request.POST.get('Audio','').strip()
        Audio_type = request.POST.get('Audio_type','').strip()
        Change_play_order = request.POST.get('Change_play_order','').strip()
        Copy_IFO = request.POST.get('Copy_IFO','').strip()
        Display_forced_sub = request.POST.get('Display_forced_sub','').strip()
        Jump_menu = request.POST.get('Jump_menu','').strip()
        Jump_main = request.POST.get('Jump_main','').strip()

        Remove_DTS = request.POST.get('Remove_DTS','').strip()
        Path_player = request.POST.get('Path_player','').strip()
        Preserve_menu_disc2 = request.POST.get('Preserve_menu_disc2','').strip()
        Remove_menu = request.POST.get('Remove_menu','').strip()
        Remove_PGC = request.POST.get('Remove_PGC','').strip()
        Rewind = request.POST.get('Rewind','').strip()
        Subtitle = request.POST.get('Subtitle','').strip()
        Title = request.POST.get('Title','').strip()
        Volume = request.POST.get('Volume','').strip()

        case.update(Num = Num, Num_test_link = Num_test_link, Iso_type = Iso_type, Mode = Mode, Src_iso = Src_iso, Dest_type = Dest_type, Out_disc = Out_disc, Profile = Profile, Enable_2Dto3D = Enable_2Dto3D, \
               Remove_HD_audio = Remove_HD_audio, Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1, Video_decoder_MPEG2 = Video_decoder_MPEG2, \
               Video_encoder_H264 = Video_encoder_H264, BD3D_convert_type = BD3D_convert_type, Compress_to_AC3 = Compress_to_AC3, DVDFab_description = DVDFab_description, Src_folder = Src_folder, \
               Src_path = Src_path, Audio = Audio, Audio_type = Audio_type, Change_play_order = Change_play_order, Copy_IFO = Copy_IFO, Display_forced_sub = Display_forced_sub, \
               Jump_menu = Jump_menu, Jump_main = Jump_main, Remove_DTS= Remove_DTS, Path_player = Path_player, Preserve_menu_disc2 = Preserve_menu_disc2, Remove_menu = Remove_menu, \
               Remove_PGC = Remove_PGC, Rewind = Rewind, Subtitle = Subtitle, Title = Title, Volume = Volume)
        return HttpResponseRedirect('/case/') 
    else:
        case = Case.objects.get(id = param1)
        return render_to_response('update_case.html',locals())   


def update_client(request,param1):
    client = Client.objects.get(id = param1)
    if request.method == "POST":
        PC_name = request.POST.get('PC_name', '').strip()
        PC_ip = request.POST.get('PC_ip','').strip()
        Dvdfab_path = request.POST.get('Dvdfab_path','').strip()
        Dest_path = request.POST.get('Dest_path','').strip()
    
        client.PC_name = PC_name
        client.PC_ip = PC_ip
        client.Dvdfab_path = Dvdfab_path
        client.Dest_path = Dest_path
        client.save()
        #client.update(PC_name = PC_name, PC_ip = PC_ip, Dvdfab_path = Dvdfab_path, Dest_path = Dest_path)
        return HttpResponseRedirect('/client/')
    return render_to_response('update_client.html',{'client':client, 'param1':param1})
    
    

def update_version(request,param1):
    version = Versions.objects.get(id = param1)
    if request.method == "POST":
        version.Version = request.POST.get('Version','').strip()
        version.Create_time = request.POST.get('Create_time','').strip()
        version.Description = request.POST.get('Description','').strip()
        version.Notes = request.POST.get('Notes','').strip()
        version.save()
        return HttpResponseRedirect('/version/')
    return render_to_response('update_version.html',locals())


def update_BD(request,param1):
    if request.method == "POST":
        bd = Samples.objects.filter(id = param1)
        Name = request.POST.get('Name','').strip()
        Video_info = request.POST.get('Video_info','').strip()
        Audio_info = request.POST.get('Audio_info','').strip()
        File_size = request.POST.get('File_size','').strip()
        Channel = request.POST.get('Channel','').strip()
        Framerate = request.POST.get('Framerate','').strip()
        Standard = request.POST.get('Standard','').strip()
        Scan_type = request.POST.get('Scan_type','').strip()
        Numbers_jar = request.POST.get('Numbers_jar','').strip()
        Company = request.POST.get('Company','').strip()
        Locations = request.POST.get('Locations','').strip()
        Description = request.POST.get('Description','').strip()
        Volume_label = request.POST.get('Volume_label','').strip()
    
        bd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
                Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
        return HttpResponseRedirect('/BD/')
    else:
        bd = Samples.objects.get(id = param1)
        return render_to_response('update_BD.html',locals())


def update_DVD(request,param1):
    if request.method == "POST":
        dvd = DVD_samples.objects.filter(id = param1)
        Name = request.POST.get('Name','').strip()
        Video_info = request.POST.get('Video_info','').strip()
        Audio_info = request.POST.get('Audio_info','').strip()
        File_size = request.POST.get('File_size','').strip()
        Channel = request.POST.get('Channel','').strip()
        Framerate = request.POST.get('Framerate','').strip()
        Standard = request.POST.get('Standard','').strip()
        Scan_type = request.POST.get('Scan_type','').strip()
        Company = request.POST.get('Company','').strip()
        Locations = request.POST.get('Locations','').strip()
        Description = request.POST.get('Description','').strip()
        Volume_label = request.POST.get('Volume_label','').strip()
    
        dvd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, Scan_type = Scan_type, \
                     Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
        return HttpResponseRedirect('/DVD/')
    else:
        dvd = DVD_samples.objects.get(id = param1)
        return render_to_response('update_DVD.html',locals())


def update_BD3D(request,param1):
    if request.method == "POST":
        bd3d = BD3D_samples.objects.filter(id = param1)
        Name = request.POST.get('Name','').strip()
        Video_info = request.POST.get('Video_info','').strip()
        Audio_info = request.POST.get('Audio_info','').strip()
        File_size = request.POST.get('File_size','').strip()
        Channel = request.POST.get('Channel','').strip()
        Framerate = request.POST.get('Framerate','').strip()
        Standard = request.POST.get('Standard','').strip()
        Scan_type = request.POST.get('Scan_type','').strip()
        Numbers_jar = request.POST.get('Numbers_jar','').strip()
        Company = request.POST.get('Company','').strip()
        Locations = request.POST.get('Locations','').strip()
        Description = request.POST.get('Description','').strip()
        Volume_label = request.POST.get('Volume_label','').strip()
        bd3d.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, \
                    Scan_type = Scan_type, Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
        return HttpResponseRedirect('/BD3D/')
    else:
        bd3d = BD3D_samples.objects.get(id = param1)
        return render_to_response('update_BD3D.html',locals())
 
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
    Name = request.GET.get('Name','').strip()
    Video_info = request.GET.get('Video_info','').strip()
    Audio_info = request.GET.get('Audio_info','').strip()
    File_size = request.GET.get('File_size','').strip()
    Channel = request.GET.get('Channel','').strip()
    Framerate = request.GET.get('Framerate','').strip()
    Standard = request.GET.get('Standard','').strip()
    Scan_type = request.GET.get('Scan_type','').strip()
    Numbers_jar = request.GET.get('Numbers_jar','').strip()
    Company = request.GET.get('Company','').strip()
    Locations = request.GET.get('Locations','').strip()
    Description = request.GET.get('Description','').strip()
    Volume_label = request.GET.get('Volume_label','').strip()
     
    bd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard, \
              Scan_type = Scan_type, Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/all_samples/')


def update_all_DVD(request,param1):
    dvd = DVD_samples.objects.filter(id = param1)          
    Name = request.GET.get('Name','').strip()
    Video_info = request.GET.get('Video_info','').strip()
    Audio_info = request.GET.get('Audio_info','').strip()
    File_size = request.GET.get('File_size','').strip()
    Channel = request.GET.get('Channel','').strip()
    Framerate = request.GET.get('Framerate','').strip()
    Standard = request.GET.get('Standard','').strip()
    Scan_type = request.GET.get('Scan_type','').strip()
    Numbers_jar = request.GET.get('Numbers_jar','').strip()
    Company = request.GET.get('Company','').strip()
    Locations = request.GET.get('Locations','').strip()
    Description = request.GET.get('Description','').strip()
    Volume_label = request.GET.get('Volume_label','').strip()
     
    dvd.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard,\
               Scan_type = Scan_type, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/all_samples/')


def update_all_BD3D(request,param1):
    bd3d = BD3D_samples.objects.filter(id = param1)        
    Name = request.GET.get('Name','').strip()
    Video_info = request.GET.get('Video_info','').strip()
    Audio_info = request.GET.get('Audio_info','').strip()
    File_size = request.GET.get('File_size','').strip()
    Channel = request.GET.get('Channel','').strip()
    Framerate = request.GET.get('Framerate','').strip()
    Standard = request.GET.get('Standard','').strip()
    Scan_type = request.GET.get('Scan_type','').strip()
    Numbers_jar = request.GET.get('Numbers_jar','').strip()
    Company = request.GET.get('Company','').strip()
    Locations = request.GET.get('Locations','').strip()
    Description = request.GET.get('Description','').strip()
    Volume_label = request.GET.get('Volume_label','').strip()
     
    bd3d.update(Name = Name, Video_info = Video_info, Audio_info = Audio_info, File_size = File_size, Channel = Channel, Framerate = Framerate, Standard = Standard,\
                Scan_type = Scan_type, Numbers_jar = Numbers_jar, Company = Company, Locations = Locations, Description = Description, Volume_label = Volume_label)
    
    return HttpResponseRedirect('/all_samples/')


def update_session_page(request,param1):
    session = Session.objects.get(id = param1)
    return render_to_response('update_session.html',locals())


def update_session(request,param1, url):
    session = Session.objects.filter(id = param1)
    Num = request.GET.get('Num','').strip()
    Sub_num = request.GET.get('Sub_num','').strip()
    Iso_type = request.GET.get('Iso_type','').strip()
    Mode = request.GET.get('Mode','').strip()
    Src_path = request.GET.get('Src_path','').strip()
    Dest_path = request.GET.get('Dest_path','').strip()
    PC_name = request.GET.get('PC_name','').strip()
    Dvdfab_path = request.GET.get('Dvdfab_path','').strip()
    Audio = request.GET.get('Audio','').strip()
    Audio_type = request.GET.get('Audio_type','').strip()
    
    Change_play_order = request.GET.get('Change_play_order','').strip()
    Copy_IFO = request.GET.get('Copy_IFO','').strip()
    Display_forced_sub = request.GET.get('Display_forced_sub','').strip()
    Jump_menu = request.GET.get('Jump_menu','').strip()
    Jump_main = request.GET.get('Jump_main','').strip()
    Out_disc = request.GET.get('Out_disc','').strip()
    Path_player = request.GET.get('Path_player','').strip()
    Preserve_menu_disc2 = request.GET.get('Preserve_menu_disc2','').strip()
    Profile = request.GET.get('Profile','').strip()
    
    Remove_DTS = request.GET.get('Remove_DTS','').strip()
    Remove_HD_audio = request.GET.get('Remove_HD_audio','').strip()
    Remove_menu = request.GET.get('Remove_menu','').strip()
    Remove_PGC = request.GET.get('Remove_PGC','').strip()
    Rewind = request.GET.get('Rewind','').strip()
    Subtitle = request.GET.get('Subtitle','').strip()
    Title = request.GET.get('Title','').strip()
    Volume = request.GET.get('Volume','').strip()
    
    Video_decoder_H264 = request.GET.get('Video_decoder_H264','').strip()
    Video_decoder_VC1 = request.GET.get('Video_decoder_VC1','').strip()
    Video_decoder_MPEG2 = request.GET.get('Video_decoder_MPEG2','').strip()
    Video_encoder_H264 = request.GET.get('Video_encoder_H264','').strip()
    DVDFab_description = request.GET.get('DVDFab_description','').strip()
    
    Start_time = request.GET.get('Start_time','').strip()
    End_time = request.GET.get('End_time','').strip()
    Total_time = request.GET.get('Total_time','').strip()
    Flag = request.GET.get('Flag','').strip()
    Folder_size = request.GET.get('Folder_size','').strip()
    Init_time = request.GET.get('Init_time','').strip()
    Web_log_path = request.GET.get('Web_log_path','').strip()
    Log_folder_path = request.GET.get('Log_folder_path','').strip()
    Result = request.GET.get('Result','').strip()
    Developer = request.GET.get('Developer','').strip()
    
    Enable_2Dto3D = request.GET.get('Enable_2Dto3D','').strip()
    BD3D_convert_type = request.GET.get('BD3D_convert_type','').strip()
    Compress_to_AC3 = request.GET.get('Compress_to_AC3','').strip()
    Current_src_path = request.GET.get('Current_src_path','').strip()
    #dict = {('一月').decode('GB2312'):1, ('二月').decode('GB2312'):2, ('三月').decode('GB2312'):3, ('四月').decode('GB2312'):4, ('五月').decode('GB2312'):5, ('六月').decode('GB2312'):6,\
    #        ('七月').decode('GB2312'):7, ('八月').decode('GB2312'):8, ('九月').decode('GB2312'):9, ('十月').decode('GB2312'):10, ('十一月').decode('GB2312'):11, ('十二月').decode('GB2312'):12}
    #dict = [('一月').decode('GB2312'),'1', ('二月').decode('GB2312'),'2', ('三月').decode('GB2312'),'3', ('四月').decode('GB2312'),'4', ('五月').decode('GB2312'),'5', ('六月').decode('GB2312'),'6',\
    #        ('七月').decode('GB2312'),'7', ('八月').decode('GB2312'),'8', ('九月').decode('GB2312'),'9', ('十月').decode('GB2312'),'10', ('十一月').decode('GB2312'),'11', ('十二月').decode('GB2312'),'12']
    dict = ['一月','1', '二月','2', '三月','3', '四月','4', '五月','5', '六月','6',\
            '七月','7', '八月','8', '九月','9', '十月','10', '十一月','11', '十二月','12']
   
    session.update(Num = Num,  Sub_num = Sub_num, Iso_type = Iso_type, Mode = Mode, Src_path = Src_path, Dest_path = Dest_path, PC_name = PC_name, Dvdfab_path = Dvdfab_path, Audio = Audio, \
                   Audio_type = Audio_type, Change_play_order = Change_play_order, Copy_IFO = Copy_IFO,  Display_forced_sub = Display_forced_sub, Jump_menu = Jump_menu, \
                   Jump_main = Jump_main, Out_disc = Out_disc, Path_player = Path_player, Preserve_menu_disc2 = Preserve_menu_disc2, Profile = Profile, Remove_DTS = Remove_DTS,\
                   Remove_HD_audio = Remove_HD_audio, Remove_menu = Remove_menu,  Remove_PGC = Remove_PGC, Rewind = Rewind, Subtitle = Subtitle, Title = Title, Volume = Volume, \
                   Video_decoder_H264 = Video_decoder_H264, Video_decoder_VC1 = Video_decoder_VC1, Video_decoder_MPEG2 = Video_decoder_MPEG2, Video_encoder_H264 = Video_encoder_H264,\
                   DVDFab_description = DVDFab_description, Start_time = Start_time, End_time = End_time, Total_time = Total_time ,Flag = Flag, Folder_size = Folder_size, \
                   Init_time = Init_time, Web_log_path = Web_log_path,  Log_folder_path = Log_folder_path, Result = Result,Developer = Developer, Enable_2Dto3D = Enable_2Dto3D,\
                   BD3D_convert_type = BD3D_convert_type, Compress_to_AC3 = Compress_to_AC3, Current_src_path = Current_src_path)
    
    return HttpResponseRedirect(url)


def update_test_result_page(request,param1): 
    session = Session.objects.get(id = param1) 
    src_iso = session.Src_path.replace("\\", "/").split('/')[-1]
    src_path = session.Src_path.replace("\\", "/").replace('/' + src_iso, '')
    if session.Iso_type.upper() == 'DVD':
        try:   
            iso = dvd = DVD_samples.objects.filter(Name = src_iso)
        except Exception, e:
            iso = dvd = ""
    elif session.Iso_type.upper() == 'BD':    
        try:
            iso = bd = Samples.objects.filter(Name = src_iso)
        except Exception, e:
            iso = bd = ""
            
    elif '3D' in src_iso.upper():
        try:
            iso = bd3d = BD3D_samples.objects.filter(Name = src_iso)
        except Exception, e:
            iso = bd3d = ""
    else:
        iso = video = ''
    
    return render_to_response('update_test_result.html',locals())


def display_bdverify_log(request):
    return render_to_response('error.html')


def display_log(request, param1):
    session = Session.objects.get(id = param1)
    log_path = 'd:/DVDfab_log'
    try:
        logname = str(session.id) + '_' + 'dvdfab_internal.log'
        filename = os.path.join(log_path, logname)
        file_content = open(filename, 'r')
        contexts = file_content.readlines()
        return render_to_response('display_log.html',{'contexts':contexts})
    except Exception, e:
        return render_to_response('error.html')


@csrf_exempt
def upload_file(request, param1):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #return HttpResponse(request.TITLES["title"])
            destination = open('/home/goland/DVDFab_log/' + request.FILES["file"].name, 'wb+')
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
        return HttpResponseRedirect('/update_test_result_page/' + param1)   
    form = UploadFileForm()
    return HttpResponseRedirect('/update_test_result_page/' + param1)

@csrf_exempt
def upload(request):
    if request.method == 'POST':
         
        form = UploadFileForm(request.POST, request.FILES)
        return HttpResponse(form)
        if form.is_valid():
            destination = open('/home/goland/DVDFab_log' + request.FILES["picture"].name, 'wb+')
            for chunk in request.FILES['picture'].chunks():
                destination.write(chunk)
            destination.close()
            return HttpResponseRedirect('/index/')   
        return HttpResponseRedirect('/case/')   
    form = UploadFileForm()
    return render_to_response("upload.html")


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
    src = r"/home/goland/develop/mysite/auto_test_tool/dvdfab_auto_test_scripts/dist"
    files = os.listdir(src) 
    for filename in files:   
        archive.write(os.path.join(src, filename), filename)
    archive.close() 
    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=dvdfab_test_scripts.zip' 
    response['Content-Length'] = temp.tell()  
    temp.seek(0) 
    return response


def download_test_zipfile_for_mac(request):
    return HttpResponse("Sorry,no mac script by now")
    temp = tempfile.TemporaryFile() 
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    src = "d:/develop/dvdfab_auto_test_scripts/dvdfab_auto_test_scripts_mac/"   
    files = os.listdir(src) 
    for filename in files:   
        archive.write(os.path.join(src, filename), filename)
    archive.close() 
    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=dvdfab_test_scripts_mac.zip' 
    response['Content-Length'] = temp.tell()  
    temp.seek(0) 
    return response

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    

def download_log_folder(request, param1):
    src_folder = "d:/DVDFab_log" 
    create_folder(src_folder)
    temp = tempfile.TemporaryFile() 
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    #for filename in files:   
    if param1 + '_dvdfab_internal.log' in os.listdir(src_folder):
        archive.write(src_folder + '/' + param1 + '_dvdfab_internal.log', param1 + '_dvdfab_internal.log')
    else:
        return render_to_response('error.html')
    archive.close() 
    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename = dvdfab_log_folder.zip' 
    response['Content-Length'] = temp.tell()  
    temp.seek(0) 
    return response

#*****************************************************************
#* @author:                                                      *
#* test                                                          *
#* description                                                   *
#*                                                               *
#*                                                               *
#*                                                               *
#*****************************************************************
def asd(filename):
    fp = open(filename, "w")
    fp.close()
    #cmd = "git clone git@10.10.2.31:autobuild/develop.git xdd_test"
    cmd = "git pull"
    subprocess.Popen(cmd, cwd = "/home/goland/xdd_test", shell = True)

@csrf_exempt
def xdd(request):
    if request.method == "POST":
        print 1111111111111111111
        asd("/home/goland/111.txt")
    else:
        asd("/home/goland/222.txt")
        print 2222222222222222222
    di = {"name":"xdd", "age":19, "sex":"male"}
    import json
    di = json.dumps(di)
    return HttpResponse(di)#, context_instance=RequestContext(request))


def test_url(request, year, template_name):
    return render_to_response(template_name)
    return HttpResponse(year)
