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

################################# BUILDSLAVES #################################


################################# CHANGESOURCES #################################
####################################GitPoller#################################
cs_gitpoller = GitPoller(#project = "aaa",
                         repourl="git_project_path_aaa",
                         #branches = ["master"],
                         branches = ['branches'],
						 pollInterval = 60,
						 gitbin = "/usr/bin/git")
						 #gitbin = "c:/Program Files/Git/bin/git.exe")								 


################################# SCHEDULERS #################################	
def dev_branch_fn_git(branch):
    branch_list = ['branches']
    if branch in branch_list:
        return branch
			
			
def isImportantAAAWindows(change):
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
	
scheduler_aaa_build = SingleBranchScheduler(name = "aaa",
                                               change_filter = ChangeFilter(branch_fn=dev_branch_fn_git),
                                               treeStableTimer = 5,
                                               builderNames = ["aaa"],
                                               fileIsImportant = isImportantAAAWindows,
                                               onlyImportant = True,
                                               properties={'owner':['1025977445@qq.com']})	

			
AAA_time = timed.Nightly(
					name = 'AAA',
					builderNames = ["aaa"],
					branch = "trunk/goland",
					hour = [200],
					minute = 200,
					dayOfWeek = [0, 1, 2, 3, 4, 5])		
					
force_builder= ForceScheduler( name="all_aaa",
	            builderNames=["aaa"])										   



################################# Factory  ################################

import dvdfab_factory_aaa
f_aaa = BuildFactory()
aaa = dvdfab_factory_aaa.Factory(f_aaa)
f_aaa = aaa.f_build()


################################# BUILDERS  #################################
aaa_build_dir = "build_aaa_dir"
b_aaa = {
		'name' : 'aaa',
		'slavename' : 'AAA',
		'builddir' : aaa_build_dir,
        'slavebuilddir' : aaa_build_dir,
		'factory' : f_aaa}

		
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
aaa_mail = MailNotifier(
					fromaddr="buildbot@goland.cn",
					sendToInterestedUsers=True,
					lookup = "goland.cn",
					mode='failing',
					relayhost = '10.10.7.151',
					smtpPort = 25,
					smtpUser = 'buildbot@goland.cn',
					smtpPassword = '123456',
					builders = ['aaa'],
					extraRecipients=['1025977445@qq.com'])					

def update_params_dict(c):
    c['slaves'].append(BuildSlave("AAA", "123456"))
    c['change_source'].append(cs_gitpoller)	
    c['schedulers'].append(scheduler_aaa_build)
    c['schedulers'].append(AAA_time)
    c['schedulers'].append(force_builder)
    c['builders'].append(b_aaa)
    c['status'].append(aaa_mail)
    return c

