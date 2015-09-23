from django.db import models
#-*- encoding:utf-8 -*-
from django.contrib import admin


class Register(models.Model):
    username = models.CharField(u"用户名",max_length=200)
    password = models.CharField(u"密码",max_length=200)
    repassword = models.CharField(u"确认密码",max_length=200)
    email = models.EmailField(u"邮箱",max_length=200)
    def __unicode__(self):
        return self.username


class Client(models.Model):
    PC_name = models.CharField(max_length = 250,blank = True,null = True)
    PC_ip = models.CharField(max_length = 250,blank = True,null = True)
    Dvdfab_path = models.CharField(max_length = 500,blank = True,null = True)
    Dest_path = models.CharField(max_length = 250,blank = True,null = True)

    def __unicode__(self):
        return  self.PC_name
    class Meta:
        ordering = ['-id']
    
    

class Web_params(models.Model):
    Days_display = models.CharField(max_length = 100, blank = True, null = True)    #days on test_result.html
    
    def __unicode__(self):
        return self.Days_display 
    class Meta:
        ordering = ['-id']
    
    
class Versions(models.Model):
    Version = models.CharField(max_length = 100, blank = True,null = True)
    Create_time = models.CharField(max_length = 100, blank = True,null = True)
    Description = models.CharField(max_length = 100, blank = True,null = True)
    Notes = models.CharField(max_length = 100, blank = True,null = True)

    def __unicode__(self):
        return self.Version
    class Meta:
        ordering = ['-id']
    
    
class Case(models.Model):
    Num = models.CharField(max_length = 50, blank = True, null = True)
    Iso_type = models.CharField(max_length = 50, blank = True, null = True)
    Mode = models.CharField(max_length = 50, blank = True, null = True)
    Src_iso = models.CharField(max_length = 500, blank = True, null = True)
    Src_folder = models.CharField(max_length = 250, blank = True, null = True)
    Src_path = models.CharField(max_length = 250, blank = True, null = True)
    Dest_type = models.CharField(max_length = 50, blank = True, null = True)
    Audio = models.CharField(max_length = 100, blank = True, null = True)
    Audio_type = models.CharField(max_length = 100, blank = True, null = True)
    
    Change_play_order = models.CharField(max_length = 20, blank = True, null = True)
    Copy_IFO = models.CharField(max_length = 20, blank = True, null = True)
    Display_forced_sub = models.CharField(max_length = 20, blank = True, null = True)
    Jump_menu = models.CharField(max_length = 20, blank = True, null = True)
    Jump_main = models.CharField(max_length = 20, blank = True, null = True)
    Out_disc = models.CharField(max_length = 50, blank = True, null = True) 
    Path_player = models.CharField(max_length = 250, blank = True, null = True)
    Preserve_menu_disc2 = models.CharField(max_length = 20, blank = True, null = True)
    Profile = models.CharField(max_length = 50, blank = True, null = True)
    
    Remove_DTS = models.CharField(max_length = 20, blank = True, null = True)
    Remove_HD_audio = models.CharField(max_length = 20, blank = True, null = True)
    Remove_menu = models.CharField(max_length = 20, blank = True, null = True)
    Remove_PGC = models.CharField(max_length = 20, blank = True, null = True)
    Rewind = models.CharField(max_length = 20, blank = True, null = True)
    Subtitle = models.CharField(max_length = 100, blank = True, null = True)
    Title = models.CharField(max_length = 100, blank = True, null = True)
    Volume = models.CharField(max_length = 100, blank = True, null = True)
    
    Num_test_link = models.CharField(max_length = 200, blank = True, null = True)
    Video_decoder_H264 = models.CharField(max_length = 20, blank = True, null = True)
    Video_decoder_VC1 = models.CharField(max_length = 20, blank = True, null = True)
    Video_decoder_MPEG2 = models.CharField(max_length = 20, blank = True, null = True)
    Video_encoder_H264 = models.CharField(max_length = 20, blank = True, null = True)
    DVDFab_description = models.CharField(max_length = 500, blank = True, null = True)
    Enable_2Dto3D = models.CharField(max_length = 20, blank = True, null = True)
    BD3D_convert_type = models.CharField(max_length = 20, blank = True, null = True)
    Compress_to_AC3 = models.CharField(max_length = 20, blank = True, null = True)
    
    def __unicode__(self):
        return self.Num
               

#bluray               
class Samples(models.Model):
    Name = models.CharField(max_length = 300, blank = True, null = True)
    Video_info = models.CharField(max_length = 500, blank = True, null = True)
    Audio_info = models.CharField(max_length = 500, blank = True, null = True)
    File_size = models.CharField(max_length = 100, blank = True, null = True)
    Channel = models.CharField(max_length = 100, blank = True, null = True)
    Framerate = models.CharField(max_length = 100, blank = True, null = True)
    
    Standard = models.CharField(max_length = 100, blank = True, null = True)
    Scan_type = models.CharField(max_length = 100, blank = True, null = True)
    Numbers_jar = models.CharField(max_length = 100, blank = True, null = True)
    
    Company = models.CharField(max_length = 100, blank = True, null = True)
    Locations = models.CharField(max_length = 100, blank = True, null = True)
    Description = models.CharField(max_length = 500, blank = True, null = True)
    Volume_label = models.CharField(max_length = 200, blank = True, null = True)
    
    def __unicode__(self):
        return self.Name
        
        
#dvd
class DVD_samples(models.Model):
    
    Name = models.CharField(max_length = 300, blank = True, null = True)
    Video_info = models.CharField(max_length = 500, blank = True, null = True)
    Audio_info = models.CharField(max_length = 500, blank = True, null = True)
    File_size = models.CharField(max_length = 100, blank = True, null = True)
    Channel = models.CharField(max_length = 100, blank = True, null = True)
    Framerate = models.CharField(max_length = 100, blank = True, null = True)
    
    Standard = models.CharField(max_length = 100, blank = True, null = True)
    Scan_type = models.CharField(max_length = 100, blank = True, null = True)
    Company = models.CharField(max_length = 100, blank = True, null = True)
    Locations = models.CharField(max_length = 100, blank = True, null = True)
    Description = models.CharField(max_length = 500, blank = True, null = True)
    Volume_label = models.CharField(max_length = 200, blank = True, null = True)
    
    def __unicode__(self):
        return self.Name
        

#bluary 3D  
class BD3D_samples(models.Model):
    
    Name = models.CharField(max_length = 300, blank = True, null = True)
    Video_info = models.CharField(max_length = 500, blank = True, null = True)
    Audio_info = models.CharField(max_length = 500, blank = True, null = True)
    File_size = models.CharField(max_length = 100, blank = True, null = True)
    Channel = models.CharField(max_length = 100, blank = True, null = True)
    Framerate = models.CharField(max_length = 100, blank = True, null = True)
    
    Standard = models.CharField(max_length = 100, blank = True, null = True)
    Scan_type = models.CharField(max_length = 100, blank = True, null = True)
    Numbers_jar = models.CharField(max_length = 100, blank = True, null = True)
    Company = models.CharField(max_length = 100, blank = True, null = True)
    Locations = models.CharField(max_length = 100, blank = True, null = True)
    Description = models.CharField(max_length = 100, blank = True, null = True)
    Volume_label = models.CharField(max_length = 200, blank = True, null = True)
    
    def __unicode__(self):
        return  self.Name
        
#test results
class Session(models.Model):
    Num = models.CharField(max_length = 20, blank = True, null = True)  
    Sub_num = models.CharField(max_length = 10, blank = True, null = True)###should define integer type
    Iso_type = models.CharField(max_length = 50, blank = True, null = True)
    Mode = models.CharField(max_length = 20, blank = True, null = True)
    Src_path = models.CharField(max_length = 500, blank = True, null = True)
    Dest_path = models.CharField(max_length = 500, blank = True, null = True)
    
    PC_name = models.CharField(max_length = 300, blank = True, null = True)
    Dvdfab_path = models.CharField(max_length = 500, blank = True, null = True)    
    Audio = models.CharField(max_length = 100, blank = True, null = True)
    Audio_type = models.CharField(max_length = 100, blank = True, null = True)  
      
    Change_play_order = models.CharField(max_length = 10, blank = True, null = True)
    Copy_IFO = models.CharField(max_length = 10, blank = True, null = True)
    Display_forced_sub = models.CharField(max_length = 10, blank = True, null = True)
    Jump_menu = models.CharField(max_length = 10, blank = True, null = True)
    Jump_main = models.CharField(max_length = 10, blank = True, null = True)
    
    Out_disc = models.CharField(max_length = 20, blank = True, null = True)    
    Path_player = models.CharField(max_length = 250, blank = True, null = True)
    Preserve_menu_disc2 = models.CharField(max_length = 10, blank = True, null = True)
    Profile = models.CharField(max_length = 50, blank = True, null = True)
    
    Remove_DTS = models.CharField(max_length = 10, blank = True, null = True)
    Remove_HD_audio = models.CharField(max_length = 10, blank = True, null = True)   
    Remove_menu = models.CharField(max_length = 10, blank = True, null = True)
    Remove_PGC = models.CharField(max_length = 10, blank = True, null = True) 
       
    Rewind = models.CharField(max_length = 10, blank = True, null = True)
    Subtitle = models.CharField(max_length = 100, blank = True, null = True)   
    Title = models.CharField(max_length = 100, blank = True, null = True)
    Volume = models.CharField(max_length = 100, blank = True, null = True)
    
    Video_decoder_H264 = models.CharField(max_length = 10, blank = True, null = True)
    Video_decoder_VC1 = models.CharField(max_length = 10, blank = True, null = True)
    Video_decoder_MPEG2 = models.CharField(max_length = 10, blank = True, null = True)
    Video_encoder_H264 = models.CharField(max_length = 10, blank = True, null = True)
    DVDFab_description = models.CharField(max_length = 500, blank = True, null = True)
    
    Start_time = models.CharField(max_length = 30, blank = True, null = True)###update this field before running dvdfab 
    End_time = models.CharField(max_length = 30, blank = True, null = True) ###update this field after running dvdfab
    Total_time = models.CharField(max_length = 30, blank = True, null = True) ##update this field after running dvdfab
    Flag = models.CharField(max_length = 100, blank = True, null = True)
    Folder_size = models.CharField(max_length = 30, blank = True, null = True)
    
    Init_time = models.DateField(auto_now_add = True)
    Web_log_path = models.CharField(max_length = 300, blank = True, null = True)
    Log_folder_path = models.CharField(max_length = 300, blank = True, null = True)
    Result = models.CharField(max_length = 500, blank = True, null = True)  
      
    Developer = models.CharField(max_length = 500, blank = True, null = True)
    Enable_2Dto3D = models.CharField(max_length = 10, blank = True, null = True)
    BD3D_convert_type = models.CharField(max_length = 10, blank = True, null = True)
    Compress_to_AC3 = models.CharField(max_length = 10, blank = True, null = True)
    Current_src_path = models.CharField(max_length = 200, blank = True, null = True)
     
    def __unicode__(self):  
        return  self.Num 
                                                            
    class Meta:
        ordering = ['-id']                                                       
               

class File(models.Model):
    
    title = models.CharField(max_length = 50, blank = True, null = True)
    photo = models.ImageField(upload_to = 'temp_media/%Y/%m/%d', blank = True, null = True)
    fatherid = models.CharField(max_length = 50, blank = True, null = True) 

    def __unicode__(self):
        return self.title



