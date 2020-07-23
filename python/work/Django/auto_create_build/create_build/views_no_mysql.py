from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import os
import logging
import subprocess


subordinatename_file = r"D:\develop\auto_create_build\subordinatename.txt"
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


def create_subordinate(subordinate_path,subordinateip,subordinatename):
    try:
        create_subordinate_cmd = "buildsubordinate create-subordinate " + subordinate_path + " " + subordinateip + ":9989 " + subordinatename + " 123456"
        os.system(create_subordinate_cmd)
        log.info("create subordinate: %s successfully!" % subordinatename)
    except Exception, e:
        log.info(str(e))    


def create_start_subordinate_script(subordinate_platform, subordinate_source_path,subordinatename):
    if subordinate_platform == "Win":
        extend_name = ".bat"
    else:
        extend_name = ""
    script_file = os.path.join(subordinate_source_path, "start_subordinate_" + subordinatename + extend_name)
    write_file(script_file, "buildsubordinate start ./" + subordinatename)
    return script_file


def start_subordinate_script(script_file):
    try:
        os.system(script_file)
        log.info("start %s successfully!" % script_file)
    except Exception, e:
        log.info(str(e))


def create_new_main(main_template,buildername,subordinatename,new_main):
    content = read_file(main_template)
    new_content = content.replace("buildername", buildername).replace("Subordinate_Name", subordinatename)
    write_file(new_main, new_content)
    log.info("create new main config file: %s successfully!" % new_main)


def import_new_main(old_main,buildername):
    new_list = []
    all_lines = read_file_lines(old_main)
    for each_line in all_lines:
        if each_line.startswith("c = BuildmainConfig = {}"):
            each_line += "\nimport main_" + buildername
        elif each_line.strip().startswith("builderNames=[") and 'name="all"' in all_lines[all_lines.index(each_line)-1]:
            each_line = each_line.replace("builderNames=[", "builderNames=['" + buildername + "',")
        new_list.append(each_line)
    new_list.append("c = main_" + buildername + ".update_params_dict(c)\n")
        
    fp = open(old_main, "w")
    for each_line in new_list:
        fp.write(each_line)
    fp.close()


def create_new_factory(subordinate_platform,scripts_path,factory_template,new_factory,script_contents1,work_dir1,description1,script_contents2,work_dir2,description2,script_contents3,work_dir3,description3):
    if not os.path.exists(scripts_path):
        os.makedirs(scripts_path)
    if subordinate_platform == "Win":
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


def restart_main(mainip):
    if mainip == "10.10.2.201":
        restart_main_cmd = ""
        current_path = r"D:\buildbot_DVDFab\main"
    elif mainip == "10.10.2.170":
        restart_main_cmd = "buildbot restart DVDFab9_developer"
        current_path = "/Buildbot_DVDFab/main"
    elif  mainip == "10.10.2.141":
        restart_main_cmd = "buildbot restart VDMC_android"
        current_path = "/home/goland/buildbot"
    subprocess.Popen(restart_main_cmd, cwd = current_path, shell = True)

    
@csrf_exempt
def create_new_build(request):
    mainip = request.POST.get("mainip", "").strip()
    subordinateip = request.POST.get("subordinateip", "").strip()
    subordinate_platform = request.POST.get("subordinate_platform", "").strip()
    subordinatename = request.POST.get("subordinatename", "").strip()
    buildername = request.POST.get("buildername", "").strip()
    #return HttpResponse(mainip)
    script_contents1 = request.POST.get("script_contents1", "").strip()
    work_dir1 = request.POST.get("work_dir1", "").strip()
    description1 = request.POST.get("description1", "").strip()
    
    script_contents2 = request.POST.get("script_contents2", "").strip()
    work_dir2 = request.POST.get("work_dir2", "").strip()
    description2 = request.POST.get("description2", "").strip()
    
    script_contents3 = request.POST.get("script_contents3", "").strip()
    work_dir3 = request.POST.get("work_dir3", "").strip()
    description3 = request.POST.get("description3", "").strip()

    if not (subordinatename and subordinateip and subordinate_platform and buildername and script_contents1 and work_dir1 and description1 and script_contents2 and work_dir2 and description2 and script_contents3 and work_dir3 and description3):
        return render_to_response("error.html")
    
    log.info("\n")
    log.info("-----------------------------begin----------------------------------")
    log.info("main ip is:%s" % mainip)
    log.info("subordinate ip is:%s" % subordinateip)
    log.info("subordinate platform is:%s" % subordinate_platform)
    log.info("subordinatename is:%s" % subordinatename)
    log.info("buildername is:%s" % buildername)
    
    all_subordinates = read_file_lines(subordinatename_file)
    if subordinatename and subordinatename + "\n" in all_subordinates:
        var_name = "subordinate"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)
    increase_file(subordinatename_file,subordinatename)
    
    all_builders = read_file_lines(buildername_file)
    if buildername and buildername + "\n" in all_builders:
        var_name = "builder"
        context = {"request":request,
                   "var_name":var_name}
        return render_to_response("duplicate.html",context)
    increase_file(buildername_file,buildername)

    if mainip == "10.10.2.201":
        old_main = r"\\10.10.2.201\DVDFab_dev\main.cfg"
        main_template = r"\\10.10.2.72\nas\other\users\xudedong\main_template.cfg"
        new_main = r"\\10.10.2.201\DVDFab_dev\main_" + buildername + ".py"
        factory_template = r"\\10.10.2.72\nas\other\users\xudedong\factory_template.py"
        new_factory = r"\\10.10.2.201\DVDFab_dev\dvdfab_factory_" + buildername + ".py"
        scripts_path = "d:/Buildbot_DVDFab/tool/" + subordinatename
        subordinate_source_path = "X:/"
        
    elif mainip == "10.10.2.170":
        old_main = r"\\10.10.2.170\DVDFab9_Developer\main.cfg"
        main_template = r"\\10.10.2.170\DVDFab9_Developer\main_template.cfg"
        new_main = r"\\10.10.2.170\DVDFab9_Developer\main_" + buildername + ".py"
        factory_template = r"\\10.10.2.170\DVDFab9_Developer\factory_template.py"
        new_factory = r"\\10.10.2.170\DVDFab9_Developer\dvdfab_factory_" + buildername + ".py"
        scripts_path = "/Volumes/DATA/Buildbot_DVDFab/tool/" + subordinatename
        subordinate_source_path = "/Volumes/X/"
        
    elif mainip == "10.10.2.141":
        old_main = r"\\10.10.2.141\VDMC_android\main.cfg"
        main_template = r"\\10.10.2.141\VDMC_android\main_template.cfg"
        new_main = r"\\10.10.2.141\VDMC_android\main_" + buildername + ".py"
        factory_template = r"\\10.10.2.141\VDMC_android\factory_template.cfg"
        new_factory = r"\\10.10.2.141\VDMC_android\dvdfab_factory_" + buildername + ".py"
        scripts_path = "/home/goland/buildbot/scripts/" + subordinatename
        subordinate_source_path = "/home/goland/buildbot"
        
    subordinate_path = os.path.join(subordinate_source_path, subordinatename)
    create_subordinate(subordinate_path,subordinateip,subordinatename)
    create_new_main(main_template,buildername,subordinatename,new_main)
    import_new_main(old_main,buildername)
    create_new_factory(subordinate_platform,scripts_path,factory_template,new_factory,script_contents1,work_dir1,description1,script_contents2,work_dir2,description2,script_contents3,work_dir3,description3)
    #TODO: restart main
    restart_main(mainip)
    script_file = create_start_subordinate_script(subordinate_platform,subordinate_source_path,subordinatename)
    start_subordinate_script(script_file)
    
    return render_to_response("success.html")












