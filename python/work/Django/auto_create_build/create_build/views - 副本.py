from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import *
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
import os
import logging
import subprocess


slavename_file = r"D:\develop\auto_create_build\slavename.txt"
buildername_file = r"D:\develop\auto_create_build\buildername.txt"

log = logging.getLogger("django")

def index(request):
    return render_to_response("index.html")
    #return render_to_response("index.html", locals())


def increase_file(filename, content):
    fp = open(filename, "a+")
    fp.write(content + "\n")
    fp.close()


def write_file(filename, content):
    fp = open(filename, "w")
    fp.write(content)
    fp.close()


def read_file(filename):
    if os.path.exists(filename):
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
    else:
        content = ""
    return content


def read_file_lines(filename):
    if os.path.exists(filename):
        fp = open(filename, "r")
        all_lines = fp.readlines()
        fp.close()
    else:
        all_lines = []
    return all_lines


def create_slave(slave_path,slaveip,slavename):
    try:
        create_slave_cmd = "buildslave create-slave " + slave_path + " " + slaveip + ":9989 " + slavename + " 123456"
        os.system(create_slave_cmd)
        log.info("create slave: %s successfully!" % slavename)
    except Exception, e:
        log.info(str(e))    


def create_start_slave_script(slave_platform, slave_source_path,slavename):
    if slave_platform == "Win":
        extend_name = ".bat"
    else:
        extend_name = ""
    script_file = os.path.join(slave_source_path, "start_slave_" + slavename + extend_name)
    write_file(script_file, "buildslave start ./" + slavename)
    return script_file


def start_slave_script(script_file):
    try:
        os.system(script_file)
        log.info("start %s successfully!" % script_file)
    except Exception, e:
        log.info(str(e))


def create_new_master(master_template,buildername,slavename,new_master):
    content = read_file(master_template)
    new_content = content.replace("buildername", buildername).replace("Slave_Name", slavename)
    write_file(new_master, new_content)
    log.info("create new master config file: %s successfully!" % new_master)


def import_new_master(old_master,buildername):
    new_list = []
    all_lines = read_file_lines(old_master)
    for each_line in all_lines:
        if each_line.startswith("c = BuildmasterConfig = {}"):
            each_line += "\nimport master_" + buildername
        elif each_line.strip().startswith("builderNames=[") and 'name="all"' in all_lines[all_lines.index(each_line)-1]:
            each_line = each_line.replace("builderNames=[", "builderNames=['" + buildername + "',")
        new_list.append(each_line)
    new_list.append("c = master_" + buildername + ".update_params_dict(c)\n")
        
    fp = open(old_master, "w")
    for each_line in new_list:
        fp.write(each_line)
    fp.close()


def create_new_factory(slave_platform,scripts_path,factory_template,new_factory,script_contents1,work_dir1,description1,script_contents2,work_dir2,description2,script_contents3,work_dir3,description3):
    if not os.path.exists(scripts_path):
        os.makedirs(scripts_path)
    if slave_platform == "Win":
        prepare_compile_file = "prepare_compile.bat"
        compile_file = "compile.bat"
        after_compile_file = "after_compile.bat"
    else:
        prepare_compile_file = "prepare_compile.sh"
        compile_file = "compile.sh"
        after_compile_file = "after_compile.sh"
        
    script1 = os.path.join(scripts_path, prepare_compile_file).replace("\\","/")
    script2 = os.path.join(scripts_path, compile_file).replace("\\","/")
    script3 = os.path.join(scripts_path, after_compile_file).replace("\\","/")
    content = read_file(factory_template)
    new_content = content.replace("work_dir1",work_dir1).replace("description1",description1).replace("script1",script1)\
                  .replace("work_dir2",work_dir2).replace("description2",description2).replace("script2",script2)\
                  .replace("work_dir3",work_dir3).replace("description3",description3).replace("script3",script3)
    write_file(new_factory, new_content)
    write_file(script1, script_contents1)
    write_file(script2, script_contents2)
    write_file(script3, script_contents3)


def restart_master(masterip):
    if masterip == "10.10.2.201":
        restart_master_cmd = ""
        current_path = r"D:\buildbot_DVDFab\master"
    elif masterip == "10.10.2.170":
        restart_master_cmd = "buildbot restart DVDFab9_developer"
        current_path = "/Buildbot_DVDFab/master"
    elif  masterip == "10.10.2.141":
        restart_master_cmd = "buildbot restart VDMC_android"
        current_path = "/home/goland/buildbot"
    subprocess.Popen(restart_master_cmd, cwd = current_path, shell = True)

    
@csrf_exempt
def create_new_build(request):
    masterip = request.POST.get("masterip", "").strip()
    slaveip = request.POST.get("slaveip", "").strip()
    slave_platform = request.POST.get("slave_platform", "").strip()
    slavename = request.POST.get("slavename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    start_method = request.POST.get("start_method", "").strip()
    #if not start_method:
    #    return HttpResponse("ok")
    #return HttpResponse(masterip)
    script_contents1 = request.POST.get("script_contents1", "").strip()
    work_dir1 = request.POST.get("work_dir1", "").strip()
    description1 = request.POST.get("description1", "").strip()
    
    script_contents2 = request.POST.get("script_contents2", "").strip()
    work_dir2 = request.POST.get("work_dir2", "").strip()
    description2 = request.POST.get("description2", "").strip()
    
    script_contents3 = request.POST.get("script_contents3", "").strip()
    work_dir3 = request.POST.get("work_dir3", "").strip()
    description3 = request.POST.get("description3", "").strip()

    if not (slavename and slaveip and slave_platform and buildername and start_method and script_contents1 and work_dir1 and description1 and script_contents2 and work_dir2 and description2 and script_contents3 and work_dir3 and description3):
        return render_to_response("error.html")
    
    log.info("\n")
    log.info("-----------------------------begin----------------------------------")
    log.info("master ip is:%s" % masterip)
    log.info("slave ip is:%s" % slaveip)
    log.info("slave platform is:%s" % slave_platform)
    log.info("slavename is:%s" % slavename)
    log.info("buildername is:%s" % buildername)

    slave_count = Build_Info.objects.filter(slavename = slavename).count()
    if slave_count >= 1:
        var_name = "slave"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)

    builder_count = Build_Info.objects.filter(buildername = buildername).count()
    if builder_count >= 1:
        var_name = "builder"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)

    
    """
    try:
        #get only one record
        Build_Info.objects.get(slavename = slavename)
        var_name = "slave"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)
    except Exception, e:
        pass
    
    try:
        Build_Info.objects.get(buildername = buildername)
        var_name = "builder"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)
    except Exception, e:
        pass
    """
        
   
    """
    all_slaves = read_file_lines(slavename_file)
    if slavename and slavename + "\n" in all_slaves:
        var_name = "slave"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)
    increase_file(slavename_file,slavename)
    
    all_builders = read_file_lines(buildername_file)
    if buildername and buildername + "\n" in all_builders:
        var_name = "builder"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)
    increase_file(buildername_file,buildername)
    """
    
    if masterip == "10.10.2.201":
        old_master = r"\\10.10.2.201\DVDFab_dev\master.cfg"
        master_template = r"\\10.10.2.72\nas\other\users\xudedong\master_template.cfg"
        new_master = r"\\10.10.2.201\DVDFab_dev\master_" + buildername + ".py"
        factory_template = r"\\10.10.2.72\nas\other\users\xudedong\factory_template.py"
        new_factory = r"\\10.10.2.201\DVDFab_dev\dvdfab_factory_" + buildername + ".py"
        scripts_path = "d:/Buildbot_DVDFab/tool/" + slavename
        slave_source_path = "X:/"
        
    elif masterip == "10.10.2.170":
        old_master = r"\\10.10.2.170\DVDFab9_Developer\master.cfg"
        master_template = r"\\10.10.2.170\DVDFab9_Developer\master_template.cfg"
        new_master = r"\\10.10.2.170\DVDFab9_Developer\master_" + buildername + ".py"
        factory_template = r"\\10.10.2.170\DVDFab9_Developer\factory_template.py"
        new_factory = r"\\10.10.2.170\DVDFab9_Developer\dvdfab_factory_" + buildername + ".py"
        scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool/" + slavename
        slave_source_path = "/Volumes/X/"
        
    elif masterip == "10.10.2.141":
        old_master = r"\\10.10.2.141\VDMC_android\master.cfg"
        master_template = r"\\10.10.2.141\VDMC_android\master_template.cfg"
        new_master = r"\\10.10.2.141\VDMC_android\master_" + buildername + ".py"
        factory_template = r"\\10.10.2.141\VDMC_android\factory_template.py"
        new_factory = r"\\10.10.2.141\VDMC_android\dvdfab_factory_" + buildername + ".py"
        scripts_path = "/home/goland/buildbot/scripts/" + slavename
        slave_source_path = "/home/goland/buildbot"

    build_info = Build_Info(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename, buildername = buildername,start_method = start_method,\
                            script_contents1 = script_contents1, work_dir1 = work_dir1, description1 = description1,script_contents2 = script_contents2,\
                            work_dir2 = work_dir2, description2 = description2,script_contents3 = script_contents3, work_dir3 = work_dir3, description3 = description3,\
                            new_master = new_master, new_factory = new_factory,scripts_path = scripts_path)
    build_info.save()

        
    slave_path = os.path.join(slave_source_path, slavename)
    create_slave(slave_path,slaveip,slavename)
    create_new_master(master_template,buildername,slavename,new_master)
    import_new_master(old_master,buildername)
    create_new_factory(slave_platform,scripts_path,factory_template,new_factory,script_contents1,work_dir1,description1,script_contents2,work_dir2,description2,script_contents3,work_dir3,description3)
    #TODO: restart master
    restart_master(masterip)
    script_file = create_start_slave_script(slave_platform,slave_source_path,slavename)
    start_slave_script(script_file)
    
    return render_to_response("success.html")



#fen ye xian shi
def display_all_records(request):
    per_page_count = 2
    nowpage = request.GET.get("nowpage","").strip()
    if nowpage == "":
        nowpage = 1
    else:
        nowpage = int(nowpage)
    count = Build_Info.objects.count()
    if count % per_page_count == 0:
        pageall = count / per_page_count
    else:
        pageall = count / per_page_count + 1
    if nowpage <= 1:
        pageup = 1
    else:
        pageup = nowpage - 1
    if nowpage + 1 >= pageall:
        pagedn = pageall
    else:
        pagedn = nowpage + 1
    start = per_page_count * (nowpage - 1)        
    build_info = Build_Info.objects.all()[start:(start + per_page_count)]
    #p = Paginator(build_info, 1)
    return render_to_response("display_all_records.html", locals())


def empty(request):
    return render_to_response("empty.html")


@csrf_exempt
def search_info(request):
    search_name = request.POST.get("search_name", "").strip()
    record_name = request.POST.get("record_name", "").strip()

    if search_name == "slavename" and record_name:
        build_info = Build_Info.objects.extra(where = ["slavename like'%%" + str(record_name) + "%%'"])
        if not build_info:
            return HttpResponseRedirect("/empty/")
        
    elif search_name == "buildername" and record_name:
        build_info = Build_Info.objects.extra(where = ["buildername like'%%" + str(record_name) + "%%'"])
        if not build_info:
            return HttpResponseRedirect("/empty/")
    else:
        return HttpResponseRedirect("/display_all_records/")
    return render_to_response("display_all_records.html",locals())



def update_info_page(request, params):
    build_info= Build_Info.objects.get(id = params)
    return render_to_response("update_info.html", locals())


@csrf_exempt
def update_info(request,params):
    build_info = Build_Info.objects.filter(id=params)
    masterip = request.POST.get("masterip", "").strip()
    slaveip = request.POST.get("slaveip", "").strip()
    slave_platform = request.POST.get("slave_platform", "").strip()
    slavename = request.POST.get("slavename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    
    start_method = request.POST.get("start_method", "").strip()
    script_contents1 = request.POST.get("script_contents1", "").strip()
    work_dir1 = request.POST.get("work_dir1", "").strip()
    description1 = request.POST.get("description1", "").strip()
    
    script_contents2 = request.POST.get("script_contents2", "").strip()
    work_dir2 = request.POST.get("work_dir2", "").strip()
    description2 = request.POST.get("description2", "").strip()
    
    script_contents3 = request.POST.get("script_contents3", "").strip()
    work_dir3 = request.POST.get("work_dir3", "").strip()
    description3 = request.POST.get("description3", "").strip()

    new_master = request.POST.get("new_master","").strip()
    new_factory = request.POST.get("new_factory","").strip()
    scripts_path = request.POST.get("scripts_path","").strip()
    if not (slavename and slaveip and slave_platform and buildername and start_method and script_contents1 and work_dir1 and description1 and script_contents2 and work_dir2 and description2 and script_contents3 and work_dir3 and description3):
        return render_to_response("error.html")

    #update database
    build_info.update(masterip = masterip, slaveip = slaveip, slave_platform = slave_platform, slavename = slavename,\
                      buildername = buildername, start_method = start_method, script_contents1 = script_contents1,\
                      work_dir1 = work_dir1, description1 = description1, script_contents2 = script_contents2, work_dir2 = work_dir2,\
                      description2 = description2, script_contents3 = script_contents3, work_dir3 = work_dir3, description3 = description3,\
                      new_master = new_master, new_factory = new_factory, scripts_path = scripts_path)

    #update conf file
    #TODO
    
    #factory file
    if masterip == "10.10.2.201":
        factory_template = r"\\10.10.2.72\nas\other\users\xudedong\factory_template.py"

    elif masterip == "10.10.2.170":
        factory_template = r"\\10.10.2.170\DVDFab9_Developer\factory_template.py"
   
    elif masterip == "10.10.2.141":
        factory_template = r"\\10.10.2.141\VDMC_android\factory_template.py"

    create_new_factory(slave_platform,scripts_path,factory_template,new_factory,script_contents1,work_dir1,description1,script_contents2,work_dir2,description2,script_contents3,work_dir3,description3)
    restart_master(masterip)

    return HttpResponseRedirect("/display_all_records/")












