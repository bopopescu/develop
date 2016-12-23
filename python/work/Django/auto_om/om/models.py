#-*- encoding:utf-8 -*-

from django.db import models
from django.contrib import admin


class EsxiPlatform(models.Manager):
    def get_query_set(self):
        return super(EsxiPlatform, self).get_query_set().filter(name = "ESXi")


class SubPlatform(models.Manager):
    def get_query_set(self):
        return super(SubPlatform, self).get_query_set().exclude(name = "ESXi")


class Platform(models.Model):
    """ 操作系统表 """
    name = models.CharField(max_length = 10, blank = True, null = True)

    objects = models.Manager()
    esxiplatform = EsxiPlatform()    
    subplatform = SubPlatform()
    
    def __unicode__(self):
        return  self.name
    #def __str__(self):
    #    return  self.name
    class Meta:
        ordering = ['id']


class Record(models.Model):
    """ 操作记录表 """
    content = models.CharField(max_length = 500, blank = True, null = True)
    
    def __unicode__(self):
        return self.id

    class Meta:
        ordering = ["-id"]


class SubManager(models.Manager):
    def get_query_set(self):
        return super(SubManager, self).get_query_set()


class PC_Info(models.Model):
    """ 服务器表 """
    platform = models.ForeignKey(Platform, related_name="platform_set")
    ip = models.CharField(max_length = 50, blank = True, null = True)
    memory = models.CharField(max_length = 50, blank = True, null = True)
    memory_left = models.CharField(max_length = 50, blank = True, null = True)
    cpu = models.CharField(max_length = 50, blank = True, null = True)
    cpu_left = models.CharField(max_length = 50, blank = True, null = True)
    hard_disk = models.CharField(max_length = 50, blank = True, null = True)
    hard_disk_left = models.CharField(max_length = 50, blank = True, null = True)
    #available_space = models.CharField(max_length = 50, blank = True, null = True)
    username = models.CharField(max_length = 50, blank = True, null = True)
    password = models.CharField(max_length = 50, blank = True, null = True)
    is_virtual = models.CharField(max_length = 10, blank = True, null = True)
    #is_virtual = models.BooleanField()
    join_date = models.CharField(max_length = 50, blank = True, null = True)
    modify_date = models.CharField(max_length = 50, blank = True, null = True)
    status = models.CharField(max_length = 10, blank = True, null = True)
    description = models.TextField()
    objects = SubManager()    

    def __unicode__(self):
        return str(self.id)
    
    def __str__(self):
        return str(self.id)

    def get_id(self):
        return self.id
    
    #@models.permalink
    #def get_update_url(self):
    def get_absolute_url(self):
        return "/update/%d/" % self.id
        return ("update", (), {"params": "1"})
        return ('update', ["1"])
        
    class Meta:
        ordering = ["-status", "ip"]
    
    class Admin:
        save_as = True
        save_on_top = True
        pass
        #search_fields = ["ip"]
        list_display = ["status", "ip", "username"]
        list_filter = ["status", "ip", "username"]


class DepartMent(models.Model):
    """ 部门表 """
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class Staff_Info(models.Model):
    """ 员工信息表 """
    platform = models.ForeignKey(Platform, related_name = "platform_staff_set")
    department = models.ForeignKey(DepartMent, related_name = "department_set")
    ip = models.CharField(max_length = 50, blank = True, null = True)
    mac_address = models.CharField(max_length = 100, blank = True, null = True)
    staff_name = models.CharField(max_length = 50, blank = True, null = True)
    asset_name = models.CharField(max_length = 100, blank = True, null = True)
    serial_num = models.CharField(max_length = 100, blank = True, null = True)
    asset_address = models.CharField(max_length = 200, blank = True, null = True)
    memory = models.CharField(max_length = 50, blank = True, null = True)
    cpu = models.CharField(max_length = 50, blank = True, null = True)
    hard_disk = models.CharField(max_length = 50, blank = True, null = True)
    join_date = models.CharField(max_length = 50, blank = True, null = True)
    modify_date = models.CharField(max_length = 50, blank = True, null = True)
    status = models.CharField(max_length = 10, blank = True, null = True)
    description = models.TextField()
    objects = SubManager()    

    def __unicode__(self):
        return str(self.id)
    
    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return "/update_staff_info/%d/" % self.id

    class Meta:
        ordering = ["asset_name"]


class IP(models.Model):
    """ ip地址表 """
    name = models.CharField(max_length = 20, blank = True, null = True)
    flag = models.CharField(max_length = 1, blank = True, null = True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return "/update_ip/%d/" % self.id

