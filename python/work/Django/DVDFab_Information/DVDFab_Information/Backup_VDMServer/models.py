from django.db import models
from django.contrib import admin


class Backup_VDMServer(models.Model):
    package_name = models.CharField(max_length = 250, blank = True, null = True)
    bootingserver_version = models.CharField(max_length = 250, blank = True, null = True)
    relayserver_version = models.CharField(max_length = 250, blank = True, null = True)
    server_version = models.CharField(max_length = 250, blank = True, null = True)
    transcode_version = models.CharField(max_length = 250, blank = True, null = True)
    vidonbase_version = models.CharField(max_length = 250, blank = True, null = True)
    vidonfs_version = models.CharField(max_length = 250, blank = True, null = True)
    vidonpeer_version = models.CharField(max_length = 250, blank = True, null = True)
    bootingserver_branch = models.CharField(max_length = 250, blank = True, null = True)
    relayserver_branch = models.CharField(max_length = 250, blank = True, null = True)
    server_branch = models.CharField(max_length = 250, blank = True, null = True)
    transcode_branch = models.CharField(max_length = 250, blank = True, null = True)
    vidonbase_branch = models.CharField(max_length = 250, blank = True, null = True)
    vidonfs_branch = models.CharField(max_length = 250, blank = True, null = True)
    vidonpeer_branch = models.CharField(max_length = 250, blank = True, null = True)
    flag = models.CharField(max_length = 250, blank = True, null = True)
    source_code_backup_path = models.CharField(max_length = 250, blank = True, null = True)
    package_folder_backup_path = models.CharField(max_length = 250, blank = True, null = True)
    description = models.CharField(max_length = 250, blank = True, null = True)

    def __unicode__(self):
        return self.package_name
    class Meta:
        ordering = ["-id"]
