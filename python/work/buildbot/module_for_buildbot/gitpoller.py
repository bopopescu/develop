from buildbot.changes.gitpoller import GitPoller
cs_gitpoller_list = []
                      
cs_gitpoller_package_WinServer_MovieBar_Main = GitPoller(repourl="git@10.10.2.31:vidon/buildtriggers.git",
branches = ['moviebar-main' , 'moviebar-pre' , 'moviebar-dev' , 'moviebar-nologo-pre' , 'moviebar-nologo-pre'],
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_package_WinServer_MovieBar_Main)
cs_gitpoller_android_vidontv_dbstar_moviebar = GitPoller(repourl="git_project_path_android_vidontv_dbstar_moviebar",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_android_vidontv_dbstar_moviebar)

cs_gitpoller_plcore_win_dev_debug = GitPoller(repourl="git_project_path_plcore_win_dev_debug",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_dev_debug)

cs_gitpoller_plcore_win_main_release = GitPoller(repourl="git_project_path_plcore_win_main_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_main_release)

cs_gitpoller_plcore_win_dev_release = GitPoller(repourl="git_project_path_plcore_win_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_dev_release)

cs_gitpoller_plcore_win_kodi_dev_release = GitPoller(repourl="git_project_path_plcore_win_kodi_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_kodi_dev_release)

cs_gitpoller_plcore_win_kodi_dev_debug = GitPoller(repourl="git_project_path_plcore_win_kodi_dev_debug",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_kodi_dev_debug)

cs_gitpoller_plcore_win_kodi_main_Release = GitPoller(repourl="git_project_path_plcore_win_kodi_main_Release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_kodi_main_Release)

cs_gitpoller_plcore_win_kodi_PrePublish_debug = GitPoller(repourl="git_project_path_plcore_win_kodi_PrePublish_debug",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_win_kodi_PrePublish_debug)

cs_gitpoller_winplayer2_dev_plcore2_thumb = GitPoller(repourl="git_project_path_winplayer2_dev_plcore2_thumb",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_winplayer2_dev_plcore2_thumb)

cs_gitpoller_package_winplayer3 = GitPoller(repourl="git@10.10.2.31:dvdfab/build.git",
branches = ['player_core2'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_package_winplayer3)

cs_gitpoller_vidonplayer_android_dev_pred_release = GitPoller(repourl="git_project_path_vidonplayer_android_dev_pred_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_dev_pred_release)

cs_gitpoller_vidonplayer_android_dev_debug = GitPoller(repourl="git_project_path_vidonplayer_android_dev_debug",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_dev_debug)

cs_gitpoller_vidonplayer_android_dev_release = GitPoller(repourl="git_project_path_vidonplayer_android_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_dev_release)

cs_gitpoller_vidonplayer_android_dev_pre_release = GitPoller(repourl="git_project_path_vidonplayer_android_dev_pre_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_dev_pre_release)

cs_gitpoller_vidonplayer_android_kodi_prepublishdev_release = GitPoller(repourl="git_project_path_vidonplayer_android_kodi_prepublishdev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_kodi_prepublishdev_release)

cs_gitpoller_vidonplayer_android_main_release = GitPoller(repourl="git_project_path_vidonplayer_android_main_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_main_release)

cs_gitpoller_vidonplayer_android_kodi_dev_debug = GitPoller(repourl="git_project_path_vidonplayer_android_kodi_dev_debug",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_kodi_dev_debug)

cs_gitpoller_vidonplayer_android_kodi_dev_release = GitPoller(repourl="git_project_path_vidonplayer_android_kodi_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_android_kodi_dev_release)

cs_gitpoller_vidonServer_Android_Dev = GitPoller(repourl="git_project_path_vidonServer_Android_Dev",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonServer_Android_Dev)

cs_gitpoller_b_t = GitPoller(repourl="git_project_path_b_t",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_b_t)

cs_gitpoller_test_git_fat = GitPoller(repourl="git_project_path_test_git_fat",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_test_git_fat)

cs_gitpoller_package_test = GitPoller(repourl="git_project_path_package_test",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_package_test)

cs_gitpoller_win_Server_Business_NoLogo_Pre = GitPoller(repourl="git_project_path_win_Server_Business_NoLogo_Pre",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_win_Server_Business_NoLogo_Pre)

cs_gitpoller_Android_vidontv_moviebar_dev_general = GitPoller(repourl="git_project_path_Android_vidontv_moviebar_dev_general",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_Android_vidontv_moviebar_dev_general)

cs_gitpoller_win_Server_Dbstar = GitPoller(repourl="git_project_path_win_Server_Dbstar",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_win_Server_Dbstar)

cs_gitpoller_vidonme_cn = GitPoller(repourl="git_project_path_vidonme_cn",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonme_cn)

cs_gitpoller_vidonme_cn = GitPoller(repourl="git@10.10.2.31:website/vidonme_cn.git",
branches = ['main'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonme_cn)

cs_gitpoller_android_vidontv_develop = GitPoller(repourl="git_project_path_android_vidontv_develop",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_android_vidontv_develop)

cs_gitpoller_android_vidontv_vbox_develop = GitPoller(repourl="git_project_path_android_vidontv_vbox_develop",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_android_vidontv_vbox_develop)

cs_gitpoller_Android_vidontv_moviebar_pre_general = GitPoller(repourl="git_project_path_Android_vidontv_moviebar_pre_general",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_Android_vidontv_moviebar_pre_general)

cs_gitpoller_plcore_android_dev_release = GitPoller(repourl="git_project_path_plcore_android_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_android_dev_release)

cs_gitpoller_plcore_android_kodi_dev_release = GitPoller(repourl="git_project_path_plcore_android_kodi_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_plcore_android_kodi_dev_release)

cs_gitpoller_vidonplayer_win_dev_release = GitPoller(repourl="git_project_path_vidonplayer_win_dev_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonplayer_win_dev_release)

cs_gitpoller_android_vidon_develop = GitPoller(repourl="git_project_path_android_vidon_develop",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_android_vidon_develop)

cs_gitpoller_te_19 = GitPoller(repourl="git_project_path_te_19",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_te_19)

cs_gitpoller_iOS_VidOn_moviebar = GitPoller(repourl="git_project_path_iOS_VidOn_moviebar",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_iOS_VidOn_moviebar)

cs_gitpoller_ios_vidon_develop = GitPoller(repourl="git_project_path_ios_vidon_develop",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_ios_vidon_develop)

cs_gitpoller_ios_vidon_release = GitPoller(repourl="git_project_path_ios_vidon_release",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_ios_vidon_release)

cs_gitpoller_android_vidontv_vbox_pre = GitPoller(repourl="git_project_path_android_vidontv_vbox_pre",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_android_vidontv_vbox_pre)

cs_gitpoller_vidonmis_build = GitPoller(repourl="git@10.10.2.31:vidon/vidonmis.git",
branches = ['web_publish'],                          
pollInterval = 10,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_vidonmis_build)

cs_gitpoller_mis_bms_build = GitPoller(repourl="git@10.10.2.31:vidon/mis_bms.git",
branches = ['debug'],                          
pollInterval = 10,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_mis_bms_build)

cs_gitpoller_auto_build_test = GitPoller(repourl="git@10.10.2.31:autobuild/auto_build.git",
branches = ['main'],                          
pollInterval = 10,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_auto_build_test)

cs_gitpoller_ubuntu_Server_Business = GitPoller(repourl="git_project_path_ubuntu_Server_Business",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_ubuntu_Server_Business)

cs_gitpoller_ubuntu_Server_Dev = GitPoller(repourl="git_project_path_ubuntu_Server_Dev",
branches = ['branches'],                          
pollInterval = 60,
gitbin = "/usr/bin/git")

cs_gitpoller_list.append(cs_gitpoller_ubuntu_Server_Dev)
