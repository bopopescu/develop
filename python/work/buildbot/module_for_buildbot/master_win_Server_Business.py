# -*- python -*-
# ex: set syntax=python:
from buildbot.process.factory import BuildFactory
from buildbot.changes.pb import PBChangeSource
from buildbot.changes.svnpoller import SVNPoller
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers import timed
from buildbot.changes.filter import ChangeFilter
from buildbot.config import BuilderConfig
from buildbot import locks
from buildbot.steps import source,shell
from buildbot.process import factory
from buildbot.buildslave import BuildSlave
from buildbot.status import html
from buildbot.status.web import auth, authz
from buildbot.status.mail import MailNotifier
from buildbot.schedulers.forcesched import ForceScheduler
from buildbot.changes.gitpoller import GitPoller
import locks

SLAVEIP = "10.10.2.73"

################################# BUILDSLAVES #################################


################################# CHANGESOURCES #################################
####################################GitPoller#################################
#cs_gitpoller = GitPoller(#project = "win_Server_Business",
#                         repourl="git_project_path_win_Server_Business",
#                         #branches = ["master"],
#                         branches = ['branches'],
#						 pollInterval = 60,
#						 gitbin = "/usr/bin/git")
#						 #gitbin = "c:/Program Files/Git/bin/git.exe")								 


################################# SCHEDULERS #################################	
def dev_branch_fn_git(branch):
    branch_list = ['branches']
    if branch in branch_list:
        return branch
			
			
def isImportantWin_Server_BusinessWindows(change):
    is_important = False
    for each_file in change.files:
        each_file = each_file.replace("\\","/")
        if each_file.startswith("/"):
            each_file = each_file[1:]
        if each_file.endswith("/"):
            each_file = each_file[:-1]
        #if each_file.startswith("DVDFab/test.txt"):
        if each_file.startswith("monitor_file_path"):
            is_important = True
            break
    return is_important
	
scheduler_win_Server_Business_build = SingleBranchScheduler(name = "win_Server_Business",
                                               change_filter = ChangeFilter(branch_fn=dev_branch_fn_git),
                                               treeStableTimer = 5,
                                               builderNames = ["win_Server_Business"],
                                               fileIsImportant = isImportantWin_Server_BusinessWindows,
                                               onlyImportant = True,
                                               properties={'owner':['hongwei.shi@goland.cn']})	

			
Win_Server_Business_time = timed.Nightly(
					name = 'Win_Server_Business',
					builderNames = ["win_Server_Business"],
					branch = "trunk/goland",
					hour = [200],
					minute = 200,
					dayOfWeek = [0, 1, 2, 3, 4])		
					
win_Server_Business_force_builder= ForceScheduler( name="all_win_Server_Business",
	            builderNames=["win_Server_Business"])										   



################################# Factory  ################################

import dvdfab_factory_win_Server_Business
f_win_Server_Business = BuildFactory()
win_Server_Business = dvdfab_factory_win_Server_Business.Factory(f_win_Server_Business)
f_win_Server_Business = win_Server_Business.f_build()

def get_lock(build_lock_dict):
    db_lock = ""
    db_lock_ip = "db_lock_" + SLAVEIP.strip().split(".")[-1]
    if db_lock_ip in build_lock_dict.keys():
        db_lock = build_lock_dict[db_lock_ip]
    return db_lock

db_lock = get_lock(locks.build_lock_dict)
################################# BUILDERS  #################################
win_Server_Business_build_dir = "build_win_Server_Business_dir"
b_win_Server_Business = {
		'name' : 'win_Server_Business',
		'slavename' : 'Win_Server_Business',
		'builddir' : win_Server_Business_build_dir,
                'slavebuilddir' : win_Server_Business_build_dir,
	        'locks' : [db_lock.access("exclusive")],
		'factory' : f_win_Server_Business}

		
################################# STATUS TARGETS  #################################
authz_cfg=authz.Authz(
    # change any of these to True to enable; see the manual for more
    # options
	auth=auth.BasicAuth([('admin', 'admin_123456')]),
    gracefulShutdown = False,
    forceBuild = 'auth', # use this to test your slave once it is set up
    forceAllBuilds = False,
    pingBuilder = False,
    stopBuild = 'auth',
    stopAllBuilds = False,
    cancelPendingBuild = 'auth',
)

################################# PROJECT MailNotifier #################################
win_Server_Business_mail = MailNotifier(
					fromaddr="buildbot@goland.cn",
					sendToInterestedUsers=True,
					lookup = "goland.cn",
					mode='failing',
					relayhost = '10.10.7.100',
					smtpPort = 25,
					smtpUser = 'buildbot@goland.cn',
					smtpPassword = '123456',
					builders = ['win_Server_Business'],
					extraRecipients=['hongwei.shi@goland.cn'])					



def update_params_dict(c):
    c['slaves'].append(BuildSlave("Win_Server_Business", "123456"))
    #c['change_source'].append(cs_gitpoller)	
    c['schedulers'].append(scheduler_win_Server_Business_build)
    c['schedulers'].append(Win_Server_Business_time)
    c['schedulers'].append(win_Server_Business_force_builder)
    c['builders'].append(b_win_Server_Business)
    c['status'].append(win_Server_Business_mail)
    return c

