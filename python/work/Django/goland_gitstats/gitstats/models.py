#-*- encoding:utf-8 -*-

from django.db import models
from django.contrib import admin


#所有的作者保存到一个表中
class Author(models.Model):
    name = models.CharField(max_length = 100,blank = True,null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']
        

#所有的工程保存到一个表中
class Project(models.Model):
    name = models.CharField(max_length = 1000,blank = True,null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']
        
        
#所有的生成的安装包保存到一个表中
class Package(models.Model):
    name = models.CharField(max_length = 250,blank = True,null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']


#所有的作者保存到一个表中
class Commit_Record(models.Model):
    author = models.ForeignKey(Author, related_name = "author_set")
    project = models.ForeignKey(Project, related_name = "project_set")
    branch_name = models.CharField(max_length = 150,blank = True,null = True)
    commit_version = models.CharField(max_length = 250,blank = True,null = True)
    commit_message = models.CharField(max_length = 2000,blank = True,null = True)
    commit_time = models.CharField(max_length = 250,blank = True,null = True)
    package_path = models.CharField(max_length = 500,blank = True,null = True)
    flag = models.CharField(max_length = 100,blank = True,null = True)

    def __unicode__(self):
        return  self.id
    class Meta:
        ordering = ['-id']



#保存验证结果
class Verification_Result(models.Model):
    name = models.CharField(max_length = 5,blank = True,null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']


#测试结果 保存测试人员填写的数据
class Test_Result(models.Model):
    commit_user = models.CharField(max_length = 150,blank = True,null = True)
    product = models.CharField(max_length = 250,blank = True,null = True)
    branch_name = models.CharField(max_length = 500,blank = True,null = True)
    package_name = models.CharField(max_length = 500,blank = True,null = True)
    package_path = models.CharField(max_length = 500,blank = True,null = True)
    plcore_branch = models.CharField(max_length = 500,blank = True,null = True)
    join_time = models.CharField(max_length = 500,blank = True,null = True)
    #changelog = models.TextField(max_length = 10000,blank = True,null = True)
    #verification_result = models.TextField(max_length = 5000,blank = True,null = True)
    #remark_explantion = models.TextField(max_length = 10000,blank = True,null = True)
    supplement_explantion = models.TextField(max_length = 10000,blank = True,null = True)

    def __unicode__(self):
        return  self.id
    class Meta:
        ordering = ['-id']


#保存验证结果
class Changelog(models.Model):
    test_result = models.ForeignKey(Test_Result, related_name = "test_result_set")
    #verification_result = models.ForeignKey(Verification_Result, related_name = "verification_result_set")
    verification_result = models.CharField(max_length = 5,blank = True,null = True)
    content = models.CharField(max_length = 5000,blank = True,null = True)
    remark_explantion = models.CharField(max_length = 5000,blank = True,null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']




#产品的名字保存到一个表中,这个是在web页面上，由开发人员添加的
class Product(models.Model):
    commit_record = models.ManyToManyField(Commit_Record)
    name = models.CharField(max_length = 250,blank = True,null = True)
    builder_name = models.CharField(max_length = 150,blank = True,null = True)
    project_name = models.CharField(max_length = 5000,blank = True,null = True)
    package_nas_path = models.CharField(max_length = 500,blank = True,null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']
