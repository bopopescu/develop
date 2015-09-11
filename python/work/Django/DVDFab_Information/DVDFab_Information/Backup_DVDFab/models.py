from django.db import models
from django.contrib import admin


class Backup_DVDFab(models.Model):
    package_name = models.CharField(max_length = 250, blank = True, null = True)
    backup_path = models.CharField(max_length = 250, blank = True, null = True)
    description = models.CharField(max_length = 250, blank = True, null = True)

    def __unicode__(self):
        return self.package_name
    class Meta:
        ordering = ["-id"]
