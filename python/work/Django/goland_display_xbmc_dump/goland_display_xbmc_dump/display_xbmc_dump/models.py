from django.db import models
from django.contrib import admin

class Dump_Info(models.Model):
    version = models.CharField(max_length = 250, blank = True, null = True)
    software_title = models.CharField(max_length = 250, blank = True, null = True)
    filepath = models.CharField(max_length = 250, blank = True, null = True)
    record_type = models.CharField(max_length = 250, blank = True, null = True)
    username = models.CharField(max_length = 250, blank = True, null = True)
    useremail = models.CharField(max_length = 250, blank = True, null = True)
    subject = models.CharField(max_length = 250, blank = True, null = True)
    content = models.CharField(max_length = 250, blank = True, null = True)
    windows_version = models.CharField(max_length = 250, blank = True, null = True)
    dvd_title = models.CharField(max_length = 250, blank = True, null = True)
    region_code = models.CharField(max_length = 250, blank = True, null = True)
    country = models.CharField(max_length = 250, blank = True, null = True)
    buy_link = models.CharField(max_length = 250, blank = True, null = True)
    filename = models.CharField(max_length = 250, blank = True, null = True)
    status = models.CharField(max_length = 250, blank = True, null = True)
    upload_time = models.CharField(max_length = 250, blank = True, null = True)
    bug_type = models.CharField(max_length = 250, blank = True, null = True)
    flag = models.CharField(max_length = 250, blank = True, null = True)
    sample = models.CharField(max_length = 250, blank = True, null = True)
    description = models.CharField(max_length = 250, blank = True, null = True)
    Init_time = models.DateField(auto_now_add = True)
    logname1 = models.CharField(max_length = 250, blank = True, null = True)
    logname2 = models.CharField(max_length = 250, blank = True, null = True)
    logname3 = models.CharField(max_length = 250, blank = True, null = True)
    logname4 = models.CharField(max_length = 250, blank = True, null = True)
    stack_file = models.CharField(max_length = 250, blank = True, null = True)
    stack_file1 = models.CharField(max_length = 250, blank = True, null = True)

    def __unicode__(self):
        return self.filename
    class Meta:
        ordering = ["-id"]
		
		
class Web_params(models.Model):
    All_Record = models.CharField(max_length = 1000, blank = True, null = True)
    To_Day = models.CharField(max_length = 1000, blank = True, null = True)
    product = models.CharField(max_length = 250, blank = True, null = True)
    username = models.CharField(max_length = 250, blank = True, null = True)
    useremail = models.CharField(max_length = 250, blank = True, null = True)
    chipid = models.CharField(max_length = 250, blank = True, null = True)
	
    def __unicode__(self):
       return self.All_Record 
    class Meta:
       ordering = ['-id']

