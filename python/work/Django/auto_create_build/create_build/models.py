from django.db import models
from django.contrib import admin


class Register(models.Model):
    username = models.CharField(u"用户名", max_length = 200)
    passwd = models.CharField(u"密码", max_length = 200)
    repasswd = models.CharField(u"确认密码", max_length = 200)
    email = models.EmailField(u"邮箱地址",max_length = 200)
    def __unicode__(self):
        return self.username
    

class Build_Steps(models.Model):
    build_info_id = models.CharField(max_length = 5000, blank = True, null = True)
    script_content = models.CharField(max_length = 5000, blank = True, null = True)
    slave_script_file = models.CharField(max_length = 5000, blank = True, null = True)
    work_dir = models.CharField(max_length = 1000, blank = True, null = True)
    description = models.CharField(max_length = 1000, blank = True, null = True)


class Build_Info(models.Model):
    masterip = models.CharField(max_length = 100, blank = True, null = True)
    slaveip = models.CharField(max_length = 100, blank = True, null = True)
    slave_platform = models.CharField(max_length = 100, blank = True, null = True)
    slavename = models.CharField(max_length = 100, blank = True, null = True)
    buildername = models.CharField(max_length = 100, blank = True, null = True)
    start_method = models.CharField(max_length = 100, blank = True, null = True)
    username = models.CharField(max_length = 100, blank = True, null = True)
    hour = models.CharField(max_length = 100, blank = True, null = True)
    minute = models.CharField(max_length = 100, blank = True, null = True)
    git_project_path = models.CharField(max_length = 100, blank = True, null = True)
    branches = models.CharField(max_length = 100, blank = True, null = True)
    monitor_file_path = models.CharField(max_length = 100, blank = True, null = True)
    send_mail = models.CharField(max_length = 100, blank = True, null = True)
    flag = models.CharField(max_length = 100, blank = True, null = True)	
    new_master = models.CharField(max_length = 1000, blank = True, null = True)
    new_factory = models.CharField(max_length = 1000, blank = True, null = True)
    scripts_path = models.CharField(max_length = 1000, blank = True, null = True)
	
    def __unicode__(self):
        return self.slavename
    class Meta:
        ordering = ["-id"]
		
	

