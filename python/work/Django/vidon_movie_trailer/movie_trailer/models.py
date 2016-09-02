#-*- encoding:utf-8 -*-

from django.db import models
from django.contrib import admin


#movie name
class Movie_Name(models.Model):
    name = models.CharField(max_length = 500,blank = True,null = True)
    picture_path = models.CharField(max_length = 500,blank = True,null = True)
    language = models.CharField(max_length = 20, blank = True, null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']
        

class Movie_Info(models.Model):
    movie_name = models.ForeignKey(Movie_Name, related_name = "movie_name_set")
    movie_time = models.CharField(max_length = 100,blank = True,null = True)
    trailer_order = models.CharField(max_length = 500,blank = True,null = True)
    address_high_definition = models.CharField(max_length = 500, blank = True, null = True)
    address_480p = models.CharField(max_length = 500,blank = True,null = True)
    address_720p = models.CharField(max_length = 500,blank = True,null = True)
    address_1080p = models.CharField(max_length = 500,blank = True,null = True)
    url_high_definition = models.CharField(max_length = 500, blank = True, null = True)
    url_480p = models.CharField(max_length = 500,blank = True,null = True)
    url_720p = models.CharField(max_length = 500,blank = True,null = True)
    url_1080p = models.CharField(max_length = 500,blank = True,null = True)

    def __unicode__(self):
        return  self.id
    class Meta:
        ordering = ['-id']
        
#movie name
class Movie_Name_ZH(models.Model):
    name = models.CharField(max_length = 500,blank = True,null = True)
    picture_path = models.CharField(max_length = 500,blank = True,null = True)
    language = models.CharField(max_length = 20, blank = True, null = True)

    def __unicode__(self):
        return  self.name
    class Meta:
        ordering = ['-id']
        

class Movie_Info_ZH(models.Model):
    movie_name = models.ForeignKey(Movie_Name_ZH, related_name = "movie_name_set")
    movie_time = models.CharField(max_length = 100,blank = True,null = True)
    trailer_order = models.CharField(max_length = 500,blank = True,null = True)
    address_high_definition = models.CharField(max_length = 500, blank = True, null = True)
    address_480p = models.CharField(max_length = 500,blank = True,null = True)
    address_720p = models.CharField(max_length = 500,blank = True,null = True)
    address_1080p = models.CharField(max_length = 500,blank = True,null = True)
    url_high_definition = models.CharField(max_length = 500, blank = True, null = True)
    url_480p = models.CharField(max_length = 500,blank = True,null = True)
    url_720p = models.CharField(max_length = 500,blank = True,null = True)
    url_1080p = models.CharField(max_length = 500,blank = True,null = True)
    download_url = models.CharField(max_length = 500, blank = True,null = True)

    def __unicode__(self):
        return  self.id
    class Meta:
        ordering = ['-id']
        
