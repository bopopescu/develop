#-*- encoding:utf-8 -*-  
#@PydevCodeAnalysisIgnore
from buildbot.process.factory import BuildFactory
from buildbot.steps.source import SVN
from buildbot.steps.shell import ShellCommand
from buildbot.steps.vstudio import VS2008

#from get_data_201 import get_build_porj_filepath, get_update_url_folder
import get_data_201
import include_201 as CONSTANT
import os.path, time
#BranchName/Project/Filepath
#eg. http://divmod.org/svn/Divmod/trunk/Nevow/formless/webform.py
#    http://divmod.org/svn/Divmod/branches/1.5.x/Nevow/formless/webform.py
def my_file_splitter(path):
    pieces = path.split('/')
    if pieces[0] == 'trunk':
        branch = None
        pieces.pop(0) # remove 'trunk'
    elif pieces[0] == 'branches':
        pieces.pop(0) # remove 'branches'
        # grab branch name
        branch = 'branches/' + pieces.pop(0)
    else:
        return None # something weird
    projectname = pieces.pop(0)
    if projectname != 'Nevow':#only monitor "Nevow"
        return None # wrong project
    return (branch, '/'.join(pieces))

"""
folders_update = ["bin", "include", "lib", "lib_release", "lib_release_test", \
                      "libAppUI", "libprofile2", "libprofile", "libmmedia", "libmmediautil", "libmwork", "libDVDExtendLayer", "libTaskBase", \
                      "DVDFabWork", "DVDFabMain", "DVDFabDisc", "DVDFabBase", "DVDFabAuthor", "DVDFabProfile", \
                      "libUI_qt", "DVDFab_qt_ui", "DVDFab_qt", "libmobile"]
builder_svn_user = "auto_builder"
builder_svn_pwd = "dvdfab_builder"
base_url = "https://thinkcentre:8443/svn/develop/branches/"
default_branch = "r15710_stable/"
#VISUAL_STUDIO_EXE = '\"C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\Common7\\IDE\\devenv.com\"'
"""

    
class WinDVDFabFactoryTs(): 
    def __init__(self, f1_par):
        self.factory = f1_par   

    def get_build_rebuild(self):
        ISOTIMEFORMAT = '%H'
        timeInfo = time.strftime(ISOTIMEFORMAT, time.localtime())
        if timeInfo == "11":
            build_mode = "Rebuild"
        else:
            build_mode = "Build"
        return build_mode

    
    def get_rebuildmode():
        ISOTIMEFORMAT = '%H'
        timeInfo = time.strftime(ISOTIMEFORMAT, time.localtime())
        if timeInfo == "15":
            build_mode = True
        else:
            build_mode = False
        return build_mode
    
    def get_buildmode():
        ISOTIMEFORMAT = '%H'
        timeInfo = time.strftime(ISOTIMEFORMAT, time.localtime())
        if timeInfo == "15":
            build_mode = False
        else:
            build_mode = True
        return build_mode
    
    def f_dvdfab_branch(self):
        builder_svn_user = "auto_builder"
        builder_svn_pwd = "dvdfab_builder"

        f1 = self.factory
        work_dir = "working_branch"       
     
        #build_rebuild = self.get_build_rebuild()

        #run get_datat.py to write svn info to svninfo.log
        #step_write_svninfo = ShellCommand(command="python d:/buildbot_DVDFab/master/DVDFab_dev/get_data_201.py",
        #                      workdir = "d:/buildbot_DVDFab/master/DVDFab_dev/")
        #f1.addStep(step_write_svninfo)       
        
        #****************************************update************************************************************
        #update source code
        #base_url = "https://thinkcentre:8443/svn/develop/trunk/goland/"
        
        #update_folders = ["include", "win", "bluray", "common", "DVDFabQxLibs","mobile2", "play"]
        update_folders = ["include", "bluray", "common", "DVDFabQxLibs","mobile2"]
        update_path = "x:\\DVDFab9_Ts\\branch\\working_branch\\"
        

        update_product_win_file = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/update_product_win_file.bat",
                                              haltOnFailure = True,
                                              descriptionDone = "update product win file")
        f1.addStep(update_product_win_file)

        """
        for each_folder in update_folders:
            if each_folder == "include":
                git_pull_folder = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull.bat",
                                               haltOnFailure = True,
                                               workdir = update_path + "include",
                                               descriptionDone = "git pull " + each_folder)
            else:
                git_pull_folder = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull.bat",
                                               haltOnFailure = True,
                                               workdir = update_path + "projects\\"+ each_folder,
                                               descriptionDone = "git pull " + each_folder)
            f1.addStep(git_pull_folder)
        """
        git_pull_include = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull_include.bat",
                                        haltOnFailure = True,
                                        workdir = update_path + "include",
                                        descriptionDone = "git pull include")
        f1.addStep(git_pull_include)
        
        git_pull_bluray = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull_bluray.bat",
                                        haltOnFailure = True,
                                        workdir = update_path + "projects\\bluray",
                                        descriptionDone = "git pull bluray")
        f1.addStep(git_pull_bluray)
        
        git_pull_common = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull_common.bat",
                                        haltOnFailure = True,
                                        workdir = update_path + "projects\\common",
                                        descriptionDone = "git pull common")
        f1.addStep(git_pull_common)
        
        git_pull_DVDFabQxLibs = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull_DVDFabQxLibs.bat",
                                        haltOnFailure = True,
                                        workdir = update_path + "projects\\DVDFabQxLibs",
                                        descriptionDone = "git pull DVDFabQxLibs")
        f1.addStep(git_pull_DVDFabQxLibs)

        git_pull_mobile2 = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/git_pull_mobile2.bat",
                                        haltOnFailure = True,
                                        workdir = update_path + "projects\\mobile2",
                                        descriptionDone = "git pull mobile2")
        f1.addStep(git_pull_mobile2)

        update_win = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/update_lib_win.bat",
                                  haltOnFailure = True,
                                  workdir = update_path + "lib/win",
                                  descriptionDone = "update lib/win")
        f1.addStep(update_win)

        update_lib_mobile2 = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/update_mobile2_lib_win.bat",
                                          haltOnFailure = True,
                                          workdir = update_path + "lib/mobile2",
                                          descriptionDone = "update lib/mobile2")
        f1.addStep(update_lib_mobile2)


        update_runtime_mobile2 = ShellCommand(command="call d:/Buildbot_DVDFab/tool/bat/update_runtime_mobile2.bat",
                                          haltOnFailure = True,
                                          workdir = update_path + "projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                          descriptionDone = "update Runtime_mobile2")
        f1.addStep(update_runtime_mobile2)


        
           
        #record current svn revison to d:/buildbot_DVDFab/tool/log/daily_build.log
        recored_revision = ShellCommand(command="python d:/buildbot_DVDFab/tool/record_revision.py",
                              workdir = "d:/buildbot_DVDFab/tool/",
                              descriptionDone = "record svn revision")
        f1.addStep(recored_revision)
        
        #copy update_build.bat
        del_exe = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/del_DVDFab9_mobile2_exe.bat",
                              workdir = "d:/buildbot_DVDFab/tool/bat/",
                              descriptionDone = "del build/Relase/exe")
        f1.addStep(del_exe)

        #***************************************DVDFab9 Debug build************************************************************
        for sub_build_filename in CONSTANT.BUILD_SLAVE_DVDFAB_9_TS:
            l_build_pro_filepath = get_data_201.get_build_porj_filepath(sub_build_filename)
            if l_build_pro_filepath:
                for each_row in l_build_pro_filepath:
                    if len(each_row[2]) != 0:
                        s_config = each_row[2]
                        s_config = s_config[:1].upper() +  s_config[1:]
                        if s_config.find("mobile2") == -1:
                            s_config = "Debug"
                        else:
                            s_config = "Debug_mobile2"                        
                    else:
                        s_config = "Debug"
                    #s_config = "Debug"
                            
                    if os.path.splitext(str(each_row[1]))[1] == ".sln":#make a sln build                            
                        step_build_DVDFab9 = VS2008(
                                                    description             = s_config + " " +str(os.path.basename(each_row[1])),
                                                    descriptionDone         = s_config + " " +str(os.path.basename(each_row[1])),
                                                    mode                =  "build",
                                                    projectfile         = each_row[1],
                                                    config              = s_config,
                                                    arch                = "x86",
                                                    haltOnFailure       = True)
                    else:#make a vcproj build
                        s_main_projname = os.path.basename(str(each_row[1])).split(".")[0]
                        if s_main_projname.lower() == "dvdfabui" or s_main_projname.lower() == "libmobile": 
                            step_build_DVDFab9 = VS2008(
                                                        description             = s_config + " " +str(os.path.basename(each_row[1])),
                                                        descriptionDone         = s_config + " " +str(os.path.basename(each_row[1])),
                                                        mode                = "rebuild",
                                                        projectfile         = each_row[1],
                                                        project             = each_row[0],
                                                        config              = s_config,
                                                        arch                = "x86",
                                                        haltOnFailure       = True)
                        else:
                            step_build_DVDFab9 = VS2008(
                                                        description             = s_config + " " +str(os.path.basename(each_row[1])),
                                                        descriptionDone         = s_config + " " +str(os.path.basename(each_row[1])),
                                                        mode                =  "build",
                                                        projectfile         = each_row[1],
                                                        project             = each_row[0],
                                                        config              = s_config,
                                                        arch                = "x86",
                                                        haltOnFailure       = True)
                                                        
                    f1.addStep(step_build_DVDFab9)
                    
        #commit lib/win/debug
        ci_debug = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_debug_mobile2.bat",
                              workdir = "d:/buildbot_DVDFab/tool/bat/",
                              descriptionDone = "commit debug")
        f1.addStep(ci_debug)

        #git push include debug
        git_push_debug = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/git_push.bat",
                              workdir = "x:/DVDFab9_Ts/branch/working_branch/include",
                              descriptionDone = "git push debug")
        f1.addStep(git_push_debug)
       
        #***************************************Make DVDFab9 Release and Release_mobile2 build****************************************************
        for sub_build_filename in CONSTANT.BUILD_SLAVE_DVDFAB_9_TS:
            l_build_pro_filepath = get_data_201.get_build_porj_filepath(sub_build_filename)
            if l_build_pro_filepath:
                for each_row in l_build_pro_filepath:
                    if len(each_row[2]) != 0:
                        s_config = each_row[2]
                        s_config = s_config[:1].upper() +  s_config[1:]
                        if s_config.find("mobile2") == -1:
                            s_config = "Release"
                        else:
                            s_config = "Release_mobile2"                        
                    else:
                        s_config = "Release"
                            
                    if os.path.splitext(str(each_row[1]))[1] == ".sln":#make a sln build                            
                        step_build_DVDFab9 = VS2008(
                                                    description             = "Release "+str(os.path.basename(each_row[1])),
                                                    descriptionDone         = "Release " +str(os.path.basename(each_row[1])),
                                                    mode                =  "build",
                                                    projectfile         = each_row[1],
                                                    config              = s_config,
                                                    arch                = "x86",
                                                    haltOnFailure       = True)
                    else:#make a vcproj build
                        s_main_projname = os.path.basename(str(each_row[1])).split(".")[0]
                        if s_main_projname.lower() == "dvdfabui" or s_main_projname.lower() == "libmobile": 
                            step_build_DVDFab9 = VS2008(
                                                        description             = "Release " +str(os.path.basename(each_row[1])),
                                                        descriptionDone         = "Release " +str(os.path.basename(each_row[1])),
                                                        mode                = "rebuild",
                                                        projectfile         = each_row[1],
                                                        project             = each_row[0],
                                                        config              = s_config,
                                                        arch                = "x86",
                                                        haltOnFailure       = True)
                        elif s_main_projname.lower() == "libmwork": 
                            step_build_DVDFab9 = VS2008(
                                                        description             = "Release " +str(os.path.basename(each_row[1])),
                                                        descriptionDone         = "Release " +str(os.path.basename(each_row[1])),
                                                        mode                = "build",
                                                        projectfile         = each_row[1],
                                                        project             = each_row[0],
                                                        config              = "Release",
                                                        arch                = "x86",
                                                        haltOnFailure       = True)
                        else:
                            step_build_DVDFab9 = VS2008(
                                                        description             = "Release "+str(os.path.basename(each_row[1])),
                                                        descriptionDone         = "Release " +str(os.path.basename(each_row[1])),
                                                        mode                =  "build",
                                                        projectfile         = each_row[1],
                                                        project             = each_row[0],
                                                        config              = s_config,
                                                        arch                = "x86",
                                                        haltOnFailure       = True)
                                                        
                    f1.addStep(step_build_DVDFab9)

        #commit lib/win/release, update build/trunk/DVDFab9_mobile2/Qt, /common
        ci_release = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_release.bat",
                              workdir = "d:/buildbot_DVDFab/tool/bat/",
                              descriptionDone = "commit Release")
        f1.addStep(ci_release)

        #update Runtime_mobile2 and Package Files
        update_package_files = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/update_Fab_package_folder.bat",
                              workdir = "d:/buildbot_DVDFab/tool/bat/",
                              descriptionDone = "update Runtime_mobile2 and Package Files")
        f1.addStep(update_package_files)

        ######################################################   DVDFab    ###########################################################
        #synchronise files from develop/DVDFabQx/Runtime to trunk/build
        sync_dvdfab9 = ShellCommand(command="python d:/buildbot_DVDFab/tool/copy_DVDFab_package_files.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "sync DVDFab9 files")
        f1.addStep(sync_dvdfab9)
		
	#close DVDFab sign
        close_DVDFab_iss_sign = ShellCommand(command="python d:/buildbot_DVDFab/tool/close_DVDFab_iss_sign.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "close DVDFab iss sign")
        #f1.addStep(close_DVDFab_iss_sign)
		
	#create DVDFab
        create_DVDFab = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/create_DVDFab.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create DVDFab")
        f1.addStep(create_DVDFab)
		
		
	#copy DVDFab to wget 
        copy_DVDFab_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/copy_DVDFab_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "copy DVDFab to wget")
        f1.addStep(copy_DVDFab_to_wget)
		
	#modify DVDFab iss and readme  
        modify_DVDFab_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/modify_DVDFab_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "modify DVDFab iss readme")
        f1.addStep(modify_DVDFab_iss_readme)
		
	#package DVDFab9 
        package_DVDFab9 = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/package_DVDFab9_mobile2_iss.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_DVDFab9)
		

		
	#ci build/DVDFab9
        ci_DVDFab9_mobile2 = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_DVDFab9_mobile2.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "checkin /build/DVDFab9")
        f1.addStep(ci_DVDFab9_mobile2)

	
        #########################################    DVDFabUSANad    ################################################

        #close DVDFabUSANad sign
        close_DVDFabUSANad_iss_sign = ShellCommand(command="python d:/buildbot_DVDFab/tool/close_DVDFabUSANad_iss_sign.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "close DVDFabUSANad iss sign")
        #f1.addStep(close_DVDFabUSANad_iss_sign)
		
	#create DVDFabUSANad
        create_DVDFabUSANad = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/create_DVDFabUSANad.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create DVDFabUSANad")
        f1.addStep(create_DVDFabUSANad)
		
		
	#copy DVDFabUSANad to wget 
        copy_DVDFabUSANad_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/copy_DVDFabUSANad_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "copy DVDFabUSANad to wget")
        f1.addStep(copy_DVDFabUSANad_to_wget)
		
	#modify DVDFabUSANad iss and readme  
        modify_DVDFabUSANad_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/modify_DVDFabUSANad_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "modify DVDFabUSANad iss readme")
        f1.addStep(modify_DVDFabUSANad_iss_readme)
		
	#package DVDFabUSANad 
        package_DVDFabUSANad = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/package_DVDFabUSANad_mobile2_iss.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_DVDFabUSANad)
		
		
	#open DVDFabUSANad sign
        open_DVDFabUSANad_iss_sign = ShellCommand(command="python d:/buildbot_DVDFab/tool/open_DVDFabUSANad_iss_sign.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "open DVDFabUSANad iss sign")
        #f1.addStep(open_DVDFabUSANad_iss_sign)

        #ci build/DVDFabUSANad
        ci_DVDFabUSANad_mobile2 = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_DVDFab9_mobile2.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "checkin /build/DVDFabUSANad")
        f1.addStep(ci_DVDFabUSANad_mobile2)
		
	#backup DVDFabUSANad
        backup_DVDFabUSANad = ShellCommand(command="python d:/buildbot_DVDFab/tool/copy_dvdfabusanad_mobile2_release.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "backup DVDFabUSANad")
        #f1.addStep(backup_DVDFabUSANad)
	


	
	########################################       BluFab        ######################################################
		
	#sync BluFab
        sync_BluFab = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/sync_BluFab.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "sync BluFab Package Files")
        f1.addStep(sync_BluFab)
		
	#close BluFab sign
        close_BluFab_iss_sign = ShellCommand(command="python d:/buildbot_DVDFab/tool/close_BluFab_iss_sign.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "close BluFab iss sign")
        #f1.addStep(close_BluFab_iss_sign)
		
	#create BluFab
        create_BluFab = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/create_BluFab.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create BluFab")
        f1.addStep(create_BluFab)
		
		
	#copy BluFab to wget 
        copy_BluFab_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/copy_BluFab_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "copy BluFab to wget")
        f1.addStep(copy_BluFab_to_wget)
		
		#modify BluFab iss and readme  
        modify_BluFab_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/modify_BluFab_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "modify BluFab iss readme")
        f1.addStep(modify_BluFab_iss_readme)
		
		#package BluFab9 
        package_BluFab9 = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/package_BluFab9_mobile2_iss.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_BluFab9)
		
		
		#open BluFab sign
        open_BluFab_iss_sign = ShellCommand(command="python d:/buildbot_DVDFab/tool/open_BluFab_iss_sign.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "open BluFab iss sign")
        #f1.addStep(open_BluFab_iss_sign)
		
		#ci build/BluFab9
        ci_BluFab9_mobile2 = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_BluFab9_mobile2.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "checkin /build/BluFab9")
        f1.addStep(ci_BluFab9_mobile2)
		
        """	
	###############################################DVDFab Retail Japan #############################################	
        ###############################################DVDFab DVD Copy #############################################	
	#create DVDFab DVD Copy
        create_DVDFab_DVD_Copy = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/create_DVDFab_DVD_Copy.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create DVDFab DVD Copy")
        f1.addStep(create_DVDFab_DVD_Copy)
		
	#copy DVDFab DVD Copy to wget 
        copy_DVDFab_DVD_Copy_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/copy_DVDFab_DVD_Copy_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy DVDFab DVD Copy to wget")
        f1.addStep(copy_DVDFab_DVD_Copy_to_wget)
		
	#modify DVDFab iss and readme  
        modify_DVDFab_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/DVDFab_Japan/modify_DVDFab_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan",
                                      descriptionDone = "modify DVDFab iss readme")
        #f1.addStep(modify_DVDFab_iss_readme)
		
	#copy package files to package path 
        package_DVDFab_DVD_Copy = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/package_DVDFab_DVD_Copy.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_DVDFab_DVD_Copy)
	
        ###############################################DVDFab BDDVD Copy #############################################	
	#create DVDFab BDDVD Copy
        create_DVDFab_BDDVD_Copy = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/create_DVDFab_BDDVD_Copy.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create DVDFab BDDVD Copy")
        f1.addStep(create_DVDFab_BDDVD_Copy)
		
	#copy DVDFab BDDVD Copy to wget 
        copy_DVDFab_BDDVD_Copy_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/copy_DVDFab_BDDVD_Copy_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy DVDFab BDDVD Copy to wget")
        f1.addStep(copy_DVDFab_BDDVD_Copy_to_wget)
		
	#modify DVDFab iss and readme  
        modify_DVDFab_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/DVDFab_Japan/modify_DVDFab_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/",
                                      descriptionDone = "modify DVDFab iss readme")
        #f1.addStep(modify_DVDFab_iss_readme)
		
	#copy package files to package path 
        package_DVDFab_BDDVD_Copy = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/package_DVDFab_BDDVD_Copy.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_DVDFab_BDDVD_Copy)
	
        ###############################################DVDFab BDDVD Premium #############################################	
	#create DVDFab BDDVD Premium
        create_DVDFab_BDDVD_Premium = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/create_DVDFab_BDDVD_Premium.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create DVDFab BDDVD Premium")
        f1.addStep(create_DVDFab_BDDVD_Premium)
		
	#copy DVDFab BDDVD Premium to wget 
        copy_DVDFab_BDDVD_Premium_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/copy_DVDFab_BDDVD_Premium_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy DVDFab BDDVD Premium to wget")
        f1.addStep(copy_DVDFab_BDDVD_Premium_to_wget)
		
	#modify DVDFab iss and readme  
        modify_DVDFab_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/DVDFab_Japan/modify_DVDFab_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/",
                                      descriptionDone = "modify DVDFab iss readme")
        #f1.addStep(modify_DVDFab_iss_readme)
		
	#copy package files to package path 
        package_DVDFab_BDDVD_Premium = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/package_DVDFab_BDDVD_Premium.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_DVDFab_BDDVD_Premium)
	
        ###############################################DVDFab BDDVD Premium Trial#############################################	
	#create DVDFab BDDVD Premium Trial
        create_DVDFab_BDDVD_Premium_Trial = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/create_DVDFab_BDDVD_Premium_Trial.bat",
                                      workdir = "X:/DVDFab9_Ts/branch/working_branch/projects/DVDFabQxLibs/DVDFabQx/Runtime_mobile2",
                                      descriptionDone = "create DVDFab BDDVD Premium Trial")
        f1.addStep(create_DVDFab_BDDVD_Premium_Trial)
		
	#copy DVDFab BDDVD Premium Trial to wget 
        copy_DVDFab_BDDVD_Premium_Trial_to_wget = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/copy_DVDFab_BDDVD_Premium_Trial_to_wget.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy DVDFab BDDVD Premium Trial to wget")
        f1.addStep(copy_DVDFab_BDDVD_Premium_Trial_to_wget)
		
	#modify DVDFab iss and readme  
        modify_DVDFab_iss_readme = ShellCommand(command="python d:/buildbot_DVDFab/tool/DVDFab_Japan/modify_DVDFab_iss_readme.py",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan",
                                      descriptionDone = "modify DVDFab iss readme")
        #f1.addStep(modify_DVDFab_iss_readme)
		
	#copy package files to package path 
        package_DVDFab_BDDVD_Premium_Trial = ShellCommand(command="call d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/package_DVDFab_BDDVD_Premium_Trial.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/DVDFab_Japan/bat/",
                                      descriptionDone = "copy package files to Common Qt")
        f1.addStep(package_DVDFab_BDDVD_Premium_Trial)

        #ci build/DVDFab retail Japan
        ci_DVDFab_retail_Japan = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_DVDFab9_mobile2.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "checkin /build/DVDFab Retail Japan")
        f1.addStep(ci_DVDFab_retail_Japan)
		
        """

        #********************************************************************************************************************************************************
        #modify intermediate files
        modify_intermediate_files = ShellCommand(command="python d:/buildbot_DVDFab/tool/modify_intermediate_files.py",
                                      workdir = "d:/buildbot_DVDFab/tool/",
                                      descriptionDone = "modify intermediate files")
        f1.addStep(modify_intermediate_files)
        
        #ci intermediate files
        ci_intermediate_files = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/ci_intermediate_files.bat",
                                      workdir = "d:/buildbot_DVDFab/tool/bat/",
                                      descriptionDone = "ci intermediate files")
        f1.addStep(ci_intermediate_files)

 
        #insert into database and backup DVDFab code
        backup_DVDFab9_Beta = ShellCommand(command="python d:/buildbot_DVDFab/tool/backup_DVDFab9_Beta.py",
                                           workdir = "d:/buildbot_DVDFab/tool",
                                           descriptionDone = "backup DVDFab code")
        f1.addStep(backup_DVDFab9_Beta)
		
        return f1
    
    def f_unittest(self):
        return

    
#Mac DVDFab autobuild factory    
class MacDVDFabFactory(): 
    def __init__(self, f1_par):
        self.factory = f1_par

    def get_buildmode(self):
        ISOTIMEFORMAT = '%H'
        timeInfo = time.strftime(ISOTIMEFORMAT, time.localtime())
        if timeInfo == "21":
            build_mode = " clean build "
        else:
            build_mode = " build "
        return build_mode

    def f_dvdfab_branch(self):
        builder_svn_user = "auto_builder"
        builder_svn_pwd = "dvdfab_builder"

        
        f1 = self.factory
        work_dir = "working_branch"
        #l_all_svninfo = []
        #l_svninfo = []

        build_rebuild = self.get_buildmode()
        
        
        """
        #update source code
        for sub_update_filename in CONSTANT.MAC_DVDFAB_FILENAME_UPDATE:
            l_update_url_folders = get_data_201.get_update_url_folder(sub_update_filename)
            #l_all_svninfo.extend(l_svninfo)#to dispaly svn info for each update folder
            #l_svninfo = []
            if l_update_url_folders:
                for each_row in l_update_url_folders:
                    f1.addStep(SVN(
                                   mode             = "update",
                                   svnurl             = str(each_row[0]),
                                   username         = builder_svn_user,
                                   password         = builder_svn_pwd,
                                   alwaysUseLatest  = True,
                                   retry            = (5, 1),
                                   workdir            = work_dir + str(each_row[1])))
        """

        base_url = "https://thinkcentre:8443/svn/develop/trunk/goland/"
        update_folders = ["include", "macosx", "DVDFab", "DVDFabMiddle", "bdnav","bluray", "common", "middle-layer", "mobile", "ui", "HomeStreamer", "player"]

        for each_folder in update_folders:
            if each_folder == "include":
                f1.addStep(SVN(
                                   mode             = "update",
                                   svnurl             = base_url + each_folder,
                                   username         = builder_svn_user,
                                   password         = builder_svn_pwd,
                                   alwaysUseLatest  = True,
                                   retry            = (5, 1),
                                   workdir            = work_dir + "/goland/" + each_folder))
            elif each_folder == "macosx":
                f1.addStep(SVN(
                                   mode             = "update",
                                   svnurl             = base_url + "lib/" + each_folder,
                                   username         = builder_svn_user,
                                   password         = builder_svn_pwd,
                                   alwaysUseLatest  = True,
                                   retry            = (5, 1),
                                   workdir            = work_dir + "/goland/lib/" + each_folder))
            else:
                f1.addStep(SVN(
                                   mode             = "update",
                                   svnurl             = base_url + "projects/" + each_folder,
                                   username         = builder_svn_user,
                                   password         = builder_svn_pwd,
                                   alwaysUseLatest  = True,
                                   retry            = (5, 1),
                                   workdir            = work_dir + "/goland/projects/" + each_folder))

        #delete .../DVDFabQtRuntime/DVDFab.app        
        del_app = ShellCommand(command="rm -rf  /Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/projects/DVDFab/DVDFabQtRuntime/DVDFab.app",
                               workdir = work_dir,
                               descriptionDone = "Delete DVDFabQtRuntime/DVDFab.app")
        f1.addStep(del_app)


        #del ..../lib/macosx/release/libUtilOS.a
        del_libuitlos = ShellCommand(command="rm -rf  /Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/lib/macosx/release/libUtilOS.a",
                               workdir = work_dir,
                               descriptionDone = "Del libUtilOS.a")
        f1.addStep(del_libuitlos)

        #**********************************************make DVDFab8 mac debug build**********************************************************
        for sub_build_filename in CONSTANT.MAC_DVDFAB_FILENAME_BUILD:
            #if sub_build_filename in ["bot_build_DVDFab_mac"]:             
            l_build_pro_filepath = get_data_201.get_build_porj_filepath(sub_build_filename)
            if l_build_pro_filepath:
                for each_row in l_build_pro_filepath:
                    if len(each_row[0]) != 0:
                        target_scheme_name = each_row[0]
                    else:
                        target_scheme_name = (os.path.split(str(each_row[1]))[1]).split(".")[0]

                    s_config = "Debug"
                                        
                    if os.path.splitext(each_row[1])[1] == ".xcworkspace":
                        cmd_line_debugbuild = "xcodebuild -workspace " + each_row[1] + \
                                            " -scheme " + target_scheme_name + \
                                             " build", + \
                                            " -configuration " + s_config
                    else:
                        s_main_projname = os.path.basename(str(each_row[1])).split(".")[0]
                        if s_main_projname.lower() != "dvdfabconsole":
                            cmd_line_debugbuild = "xcodebuild -project " + each_row[1] + \
                                                      " -target " + target_scheme_name + \
                                                      "  build -configuration " + s_config
                                
                    step_build_debug_DVDFab = ShellCommand(command = cmd_line_debugbuild, \
                                                           workdir = work_dir, \
                                                           haltOnFailure   = False, \
                                                           description             = "debug "+str(os.path.basename(each_row[1])),\
                                                           descriptionDone         = "debug "+str(os.path.basename(each_row[1])))
                                                        
                    f1.addStep(step_build_debug_DVDFab)

        #commit /lib/macosx/release
        ci_debug_mac = ShellCommand(command="svn ci /Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/lib/macosx/debug -m 'new debug lib from mac daily build'",
                                    workdir = "/Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/lib/macosx/",
                                    descriptionDone = "Commit debug lib")
        f1.addStep(ci_debug_mac)

        #commit /include
        #ci_include_mac = ShellCommand(command="svn ci /Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/include -m 'new include from mac daily build'",
                                 #workdir = "/Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/")
        #f1.addStep(ci_include_mac)
        
        #**********************************************make DVDFab8 mac build**********************************************************
        #get_build_porj_filepath: return = [[projectname, filepath, buildmode], [projectname, filepath, buildmode]]
        for sub_build_filename in CONSTANT.MAC_DVDFAB_FILENAME_BUILD:
            l_build_pro_filepath = get_data_201.get_build_porj_filepath(sub_build_filename)
            if l_build_pro_filepath:
                for each_row in l_build_pro_filepath:
                    if each_row[1].lower().find("projects/homestreamer") == -1 and each_row[1].lower().find("projects/player") == -1:
                        if len(each_row[0]) != 0:
                            target_scheme_name = each_row[0]
                        else:
                            target_scheme_name = (os.path.split(str(each_row[1]))[1]).split(".")[0]

                        if len(each_row[2]) != 0:
                            s_config = each_row[2]
                            s_config = s_config[:1].upper() +  s_config[1:]
                        else:
                            s_config = "Release"
                                        
                        if os.path.splitext(each_row[1])[1] == ".xcworkspace":
                            cmd_line = "xcodebuild -workspace " + each_row[1] + \
                                        " -scheme " + target_scheme_name + \
                                         " build ", + \
                                        " -configuration " + s_config
                                        
                                        
                        else:
                            s_main_projname = os.path.basename(str(each_row[1])).split(".")[0]
                            if s_main_projname.lower() == "dvdfab" or s_main_projname.lower() == "libmobile" or s_main_projname.lower() == "libloader":
                                cmd_line = "xcodebuild -project " + each_row[1] + \
                                            " -target " + target_scheme_name + \
                                            " clean build " + \
                                            " -configuration " + s_config
                            else:
                                cmd_line = "xcodebuild -project " + each_row[1] + \
                                            " -target " + target_scheme_name + \
                                             "  build -configuration " + s_config
                        
                        step_build_DVDFab = ShellCommand(command = cmd_line, \
                                                         workdir = work_dir, \
                                                         haltOnFailure   = False, \
                                                         description             = str(os.path.basename(each_row[1])),\
                                                         descriptionDone         = str(os.path.basename(each_row[1])))
                                                        
                        f1.addStep(step_build_DVDFab)

        #commit /lib/macosx/release
        ci_release_mac = ShellCommand(command="svn ci /Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/lib/macosx/release -m 'commit new lib daily build'",
                                      workdir = "/Volumes/X/DVDFab_mac/stable_branch/working_branch/goland/lib/macosx/",
                                      descriptionDone = "Commit release lib")
        f1.addStep(ci_release_mac)
        

        #copy DVDFab.app to daily_build     
        cp_app_dailybuild = ShellCommand(command="python /Buildbot_DVDFab/tool/mac_copy_dvdfab_app.py",
                                         workdir = "/Buildbot_DVDFab/tool/",
                                         descriptionDone = "Copy DVDFab.app")
        f1.addStep(cp_app_dailybuild)   
        #**********************************************make player mac build**********************************************************
        #make a player build  
        #get_build_porj_filepath: return = [[projectname, filepath, buildmode], [projectname, filepath, buildmode]]

        #copy bdjvm.so to system/players/dvdplayer/.
        cp_bdjvm = ShellCommand(command="/Buildbot_DVDFab/tool/bat/copy_bdjvm",
                                workdir = "/Buildbot_DVDFab/tool/bat",
                                descriptionDone = "Copy bdjvm")
        f1.addStep(cp_bdjvm)


        #del DVDFabMediaPlayer.app and FabStreamer.app
        rm_FabStreamer_DVDFabMediaPlayer = ShellCommand(command="/Buildbot_DVDFab/tool/bat/rm_player",
                                                        workdir = "/Buildbot_DVDFab/tool/bat",
                                                        descriptionDone = "rm player.app")

        f1.addStep(rm_FabStreamer_DVDFabMediaPlayer)       
        
        for sub_build_filename in CONSTANT.MAC_PLAYER_FILENAME_BUILD:
            l_build_pro_filepath = get_data_201.get_build_porj_filepath(sub_build_filename)
            if l_build_pro_filepath:
                for each_row in l_build_pro_filepath:
                    if each_row[1].lower().find("projects/homestreamer") != -1 or each_row[1].lower().find("projects/player") != -1:
                        if len(each_row[0]) != 0:
                            target_scheme_name = each_row[0]
                        else:
                            target_scheme_name = (os.path.split(str(each_row[1]))[1]).split(".")[0]

                        if len(each_row[2]) != 0:
                            s_config = each_row[2]
                            s_config = s_config[:1].upper() +  s_config[1:]
                        else:
                            s_config = "Release"
                                        
                        if os.path.splitext(each_row[1])[1] == ".xcworkspace":
                            cmd_line = "xcodebuild -workspace " + each_row[1] + \
                                        " -scheme " + target_scheme_name + \
                                        " clean build -configuration " + s_config
                                        
                                        
                        else:
                            cmd_line = "xcodebuild -project " + each_row[1] + \
                                        " -target " + target_scheme_name + \
                                       " clean build -configuration " + s_config
                        
                        step_build_Player = ShellCommand(command = cmd_line, \
                                                         workdir = work_dir, \
                                                         haltOnFailure   = False, \
                                                         description             = str(os.path.basename(each_row[1])),\
                                                         descriptionDone         = str(os.path.basename(each_row[1])))
                                                        
                        f1.addStep(step_build_Player)

        #copy DVDFab.app to daily_build     
        cp_player_dailybuild = ShellCommand(command="python /Buildbot_DVDFab/tool/mac_copy_player_app.py",
                                            workdir = "/Buildbot_DVDFab/tool/",
                                            descriptionDone = "Copy DVDFabMediaPlayer.app")
        f1.addStep(cp_player_dailybuild)        

        #**********************************************display svn info**********************************************************
        #dispaly svn info
        #dispaly_svninfo = ShellCommand(command="python /Buildbot_DVDFab/tool/mac_display_svninfo.py",
        #                               workdir = "/Buildbot_DVDFab/tool/",
        #                               descriptionDone = "Display Mac svninfo")
        #f1.addStep(dispaly_svninfo)


        #**********************************************DVDFab mac unit test*******************************************************
        #copy unittest exe to /Volumes/X/unittest/DVDFab
        cp_unit_test = ShellCommand(command="/Buildbot_DVDFab/tool/bat/copy_unittest",
                                    workdir = "/Buildbot_DVDFab/tool/bat/",
                                    descriptionDone = "cp unittest")
        #f1.addStep(cp_unit_test)

        #commit x:\unittest\DVDFab\win to http://10.10.2.62:8090/svn/DVDFab
        ci_unit_test = ShellCommand(command="ci  /Buildbot_DVDFab/unittest/DVDFab/macosx -m 'new mac unittest'",
                                    workdir = "/Buildbot_DVDFab/unittest/DVDFab",
                                    descriptionDone = "commit unittest")
        #f1.addStep(ci_unit_test)

        
        return f1
    
    def f_unittest(self):
        return  

class WinDVDFabRebuildFactory(): 
    def __init__(self, f1_par):
        self.factory = f1_par

    def f_dvdfab_branch(self):
        builder_svn_user = "auto_builder"
        builder_svn_pwd = "dvdfab_builder"

        f1 = self.factory
        work_dir = "working_branch"
        
        l_all_svninfo = []
            
        #update source code
        for sub_update_filename in CONSTANT.BOT_DVDFAB_FILENAME_UPDATE:
            l_update_url_folders, l_svninfo = get_data_201.get_update_url_folder(sub_update_filename)
            l_all_svninfo.append(l_svninfo)#to dispaly svn info for each update folder
            l_svninfo = []
            if l_update_url_folders:
                for each_row in l_update_url_folders:
                    if each_row[0].find("projects/HomeStreamer")!= -1 or each_row[0].find("projects/player") != -1:
                        f1.addStep(SVN(
                                   mode             = "update",
                                   svnurl             = str(each_row[0]),
                                   username         = builder_svn_user,
                                   password         = builder_svn_pwd,
                                   alwaysUseLatest  = True,
                                   retry            = (5, 1),
                                   workdir            = work_dir + str(each_row[1])))
                    else:
                        f1.addStep(SVN(
                                       mode             = "clobber",
                                       svnurl             = str(each_row[0]),
                                       username         = builder_svn_user,
                                       password         = builder_svn_pwd,
                                       alwaysUseLatest  = True,
                                       retry            = (5, 1),
                                       workdir            = work_dir + str(each_row[1])))
                                           
            #copy update_build.bat
            cp_bat = ShellCommand(command="call d:/buildbot_DVDFab/tool/bat/updatebuild_copy.bat",
                                  workdir = "d:/buildbot_DVDFab/tool/bat/")
            f1.addStep(cp_bat)

        
        
        #make a build  
        for sub_build_filename in CONSTANT.BOT_DVDFAB_FILENAME_BUILD:
            l_build_pro_filepath = get_data_201.get_build_porj_filepath(sub_build_filename)
            if l_build_pro_filepath:
                for each_row in l_build_pro_filepath:
                    if len(str(each_row[0])) == 0:
                        #make a build
                        step_build_DVDFab = VS2008(
                                                    mode        = "build",
                                                    projectfile    = each_row[1],
                                                    config        = "release",
                                                    arch        = "x86",
                                                    haltOnFailure    = True)
                    else:
                        step_build_DVDFab = VS2008(
                                                mode        = "build",
                                                projectfile = each_row[1],
                                                project     = each_row[0],
                                                config        = "release",
                                                arch        = "x86",
                                                haltOnFailure    = True)
                                                    
                    f1.addStep(step_build_DVDFab)


        #update package branch

        #package_username = "auto_packager"
        #package_password = "dvdfab_packager"
        #package_workdir = "x:/build/trunk/"
        #package_svnurl = "https://thinkcentre:8443/svn/build/trunk/DVDFab_alpha"
        #f1.addStep(SVN(
        #                       mode         = "clobber",
        #                       svnurl         = package_svnurl,
        #                       username         = package_username,
        #                       password         = package_password,
        #                       alwaysUseLatest  = True,
        #                       retry            = (5, 1),
        #                       workdir        = package_workdir))


        #package DVDFab using new DVDFab_Qt_new.bat
        package_DVDFab = ShellCommand(command="call x:/build/trunk/DVDFab_alpha/DVDFab_Qt.bat",
                                      workdir = " x:/build/trunk/DVDFab_alpha/")
        f1.addStep(package_DVDFab)
        

        #copy release and install to d:/DVDFab/daily_build
        cp_release = ShellCommand(command="python d:/buildbot_DVDFab/tool/copy_release_pkg.py",
                                      workdir = "d:/buildbot_DVDFab/tool/")
        f1.addStep(cp_release)
        
      
        return f1
    
    def f_unittest(self):
        return

     
