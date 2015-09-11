#-*- encoding:utf-8 -*-
import subprocess
import MySQLdb
import time, datetime
import platform
import os
import re
import socket
import logging
from ftplib import FTP

import zipfile
import ConfigParser
from shutil import Error
from shutil import copystat
from shutil import copy2
import getpass
user_name = getpass.getuser()
xml_temp = 'C:\\Users\\' + user_name + '\\AppData\\Roaming\\DVDFab9\\temp.xml'


if os.name == 'nt':
    import windows_xml
    #TESTBAT_PATH ='d:/wenjian/test.bat'
    #INI_FILE ='d:/wenjian/dvdfab_auto_tool.ini'
    current_path = os.getcwd()
    TESTBAT_PATH = current_path +'/test.bat'
    KILL_DVDFAB_PATH = current_path +'/kill_DVDFab.bat'
    #CLICK_TRY = current_path +'/click_try.bat'
    #CLICK_OK = current_path + '/click_OK.bat'
    INI_FILE = current_path + '/dvdfab_auto_tool.ini'
else:
    import myxml
    #TESTBAT_PATH = '/Users/user/Documents/test.bat'
    #INI_FILE = '/Users/user/Documents/dvdfab_auto_tool.ini'
    DVDFAB_PATH = '/Applications/"DVDFab 9.app"/Contents/MacOS/DVDFab'  
    current_path = os.getcwd()
    TESTBAT_PATH = current_path + '/test.bat'
    INI_FILE = current_path + '/dvdfab_auto_tool.ini'


def get_documents_path():
    if os.name == 'nt':
        SYSTEM_NAME = platform.platform()
        if "XP" in SYSTEM_NAME.upper():
            documents_path = os.path.expanduser("~") + "\\My Documents"
        else:
            documents_path = os.path.expanduser('~') + '\\Documents'
    else:
        documents_path = os.path.expanduser('~') + '/Documents'
    return documents_path

documents_path = get_documents_path()
LOG_FILENAME = documents_path + '/test.log'


def connect_database():    
    conn = ''
    cursor = ''
    try:
        conn = MySQLdb.connect(host = '10.10.2.11', user = 'root', passwd = '19890612')   
        conn.select_db('mysite')    
    except Exception, e:
        initlog('failed to connect database; ' + str(e))     
    else:
        cursor = conn.cursor()     
    return conn, cursor


def get_pcname():    
    pc_name = ''  
    try:   
        pc_name = socket.gethostname()       
    except Exception, e:
        initlog('failed to get PC name; ' + str(e))            
    return pc_name


def get_ip(pc_name):     
    pc_ip = ''    
    try:   
        pc_ip = socket.gethostbyname(pc_name)   
    except Exception, e:
        initlog('failed to get PC ip; ' + str(e))          
    return pc_ip


def get_client_path(pc_ip):
    pc_name = ''
    client_dest_path = ''
    conn, cursor = connect_database() 
    sql = "select PC_name, Dest_path from blog_client where PC_ip = '%s'" % pc_ip
    try:
        cursor.execute(sql)
        pc_name, client_dest_path = cursor.fetchone()   
        conn.commit() 
    except Exception, e:      
        initlog(str(e))   
    finally:
        cursor.close()   
        conn.close()       
    return pc_name, client_dest_path


def get_ip_address(pc_name):    
    client_ip = ''
    client_dest_path = ''
    conn, cursor = connect_database() 
    sql = "select PC_ip, Dest_path from blog_client where PC_name = '%s'" % pc_name 
    try:
        cursor.execute(sql)
        client_ip, client_dest_path = cursor.fetchone()   
        conn.commit() 
    except Exception, e:      
        initlog(str(e))   
    finally:
        cursor.close()   
        conn.close()       
    return client_ip, client_dest_path
  
    
def search_session_table(pc_name):    
    res = '' 
    conn, cursor = connect_database()
    sql = " select * from blog_session where  PC_name = '%s' and (Flag = 0 or Flag =  1) " % pc_name  
    try:
        cursor.execute(sql)
        res = cursor.fetchone()    
        conn.commit() 
    except Exception, e: 
        initlog('failed to search session table; ' + str(e))     
    finally:
        cursor.close()     
        conn.close()     
    return  res


def res_to_iso(res):
    if '/' in res[5]:
        module = res[5].split('/')[-2].upper()                                                #BD, DVD, BD3D, FILE
        iso = res[5].split('/')[-1]                                                           #HUGO.iso 
    else:
        module = res[5].split('\\')[-2].upper()                                                #BD, DVD, BD3D, FILE
        iso = res[5].split('\\')[-1]                                                           #HUGO.iso
    ripper_mode = res[4]
    return module, iso, ripper_mode

 
def search_iso_path(module, iso, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac):    
    src_iso_path = '' 
    try:
        if ',' in bd_path:
            bd_path_list = bd_path.split(',')
            bd_path_mac_list = bd_path_mac.split(',')
        else:
            bd_path_list = bd_path.split(';')
            bd_path_mac_list = bd_path_mac.split(';')
        
        if ',' in dvd_path:
            dvd_path_list = dvd_path.split(',')
            dvd_path_mac_list = dvd_path_mac.split(',')
        else:
            dvd_path_list = dvd_path.split(';')
            dvd_path_mac_list = dvd_path_mac.split(';')
        
        if ',' in file_path:
            file_path_list = file_path.split(',')
            file_path_mac_list = file_path_mac.split(',')
        else:
            file_path_list = file_path.split(';')
            file_path_mac_list = file_path_mac.split(';')
    except Exception, e:
        initlog('ini file is error; ' + str(e))
    
    #windows
    if os.name == 'nt':                              
        if 'DVD' == module:        
            for path in dvd_path_list:               
                for root, _, all_files in os.walk(path.strip()):
                    for onefile in all_files:                
                        if iso.upper()  == onefile.upper():                    
                            src_iso_path = os.path.join(root, onefile)  
                            return src_iso_path               
             
        elif 'VIDEO' == module:    
            for path in file_path_list:
                for root, _, all_files in os.walk(path.strip()):              
                    for onefile in all_files:                
                        if iso.upper()  == onefile.upper():
                            src_iso_path = os.path.join(root, onefile)
                            return src_iso_path 
     
        else:                                                           #bd or 3d
            for path in bd_path_list:      
                for root, _, all_files in os.walk(path.strip()): 
                    for onefile in all_files:   
                        if iso.upper()  == onefile.upper():               
                            src_iso_path = os.path.join(root, onefile)                                                    
                            return src_iso_path     
    
    #mac os          
    else:
        try:

            if not os.path.exists('/Volumes/nas2_nas2_volume3'):
                os.system('open smb://10.10.2.56')
                time.sleep(20)

            if not os.path.exists('/Volumes/nas3_nas3_Volume5'):
                os.system('open smb://10.10.2.59')
                time.sleep(20)
            if not os.path.exists('/Volumes/Nas4_Nas4_Volume4'):
                os.system('open smb://10.10.2.57')
                time.sleep(20)  
                       
        except Exception, e:
            initlog('does not execute the command to connect server; ' + str(e))
        else:                     
            for path in bd_path_mac_list:
                if not os.path.exists(path.strip()):
                    initlog(path.strip() + ' does not exist； ')     
                              
            if 'DVD' == module:        
                for path in dvd_path_mac_list:   
                    for root, _, all_files in os.walk(path.strip()):           
                        for onefile in all_files:                
                            if iso.upper()  == onefile.upper():                    
                                src_iso_path = os.path.join(root, onefile)  
                                return src_iso_path               
                 
            elif 'VIDEO' == module:    
                for path in file_path_mac_list:    
                    for root, _, all_files in os.walk(path.strip()):          
                        for onefile in all_files:                
                            if iso.upper()  == onefile.upper():
                                src_iso_path = os.path.join(root, onefile)
                                return src_iso_path 
                                    
            else:                                                           #bd or 3d
                for path in bd_path_mac_list:      
                    for root, _, all_files in os.walk(path.strip()): 
                        for onefile in all_files:   
                            if iso.upper()  == onefile.upper():               
                                src_iso_path = os.path.join(root, onefile)                                                    
                                return src_iso_path 
                     
     
def update_session_table(res, Flag, case_id, case_num, pc_name, src_iso_path = '', Start_time = '', End_time = '', Total_time = '', Folder_size = '', result = ''):    
    update_flag = True
    if src_iso_path == '':
        src_iso_path = res[5]
    if Start_time == '':
        Start_time = res[33]    
    conn, cursor = connect_database()     
    sql = "update blog_session set Current_src_path = '%s', Flag = '%d', Start_time = '%s', End_time = '%s', Total_time = '%s', Folder_size = '%s', Result = '%s' where id = '%d' and  Num = '%s' and PC_name = '%s' and (Flag = 0 or Flag =  1)" \
          % (src_iso_path, Flag, Start_time, End_time, Total_time, Folder_size, result, case_id, case_num, pc_name) 
    try:      
        cursor.execute(sql)  
        conn.commit()   
    except Exception, e: 
        initlog('failed to update session table; ' + str(e)) 
        update_flag = False
    finally:               
        cursor.close()    
        conn.close() 
    return update_flag
 
 
def update_session_flag(Flag, case_id, case_num, pc_name):
    conn, cursor = connect_database()   
    sql = "update blog_session set Flag = '%d' where id = '%d' and Num = '%s' and PC_name = '%s'" % (Flag, case_id, case_num, pc_name)
    try:      
        cursor.execute(sql)  
        conn.commit()   
    except Exception, e: 
        initlog('failed to update session table; ' + str(e)) 
    finally:               
        cursor.close()    
        conn.close() 
    
    
def get_registry_value(regpath, regkey):    
    if os.name == "nt":
        import _winreg
        value_path = ''
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, regpath, 0, _winreg.KEY_READ)
        #key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, regpath, 0, _winreg.REG_SZ)
        try: 
            (value_path, valuetype) = _winreg.QueryValueEx(key, regkey)
        except Exception, e:
            initlog('failed to get registry value; ' + str(e))  
    
        return value_path
    else:
        pass
    
    
def get_cmd_string(res, src_iso_path, client_dest_path):    
    dest_path = change_fuhao(res[6])
    if res[6]:
        Dest = '  /DEST '  + '"' + res[6] + '"'   
    else:
        Dest = '' 
        
    if res[4]:
        Mode =  '  /MODE ' + '"' + res[4] + '"'    
    else:
        Mode = ''
        
    if src_iso_path:
        Src = '   /SRC ' + '"' + src_iso_path + '"'  
    else:
        Src = ''
        
    if res[9]:   
        Audio =  '  /AUDIO ' + '"' + res[9] + '"'    
    else:
        Audio = ''

    if res[10]:
        Audio_type = '  /AUDIOTYPE ' + '"' + res[10] + '"'   
    else:
        Audio_type = ''
        
    if res[11]: 
        Change_play_order = '  /CHANGEPLAYORDER ' + '"' + res[11] + '"'  
    else:
        Change_play_order = ''  
        
    if res[12]:
        Copy_IFO = '  /COPYIFO ' + '"' + res[12] + '"'   
    else:
        Copy_IFO = '' 
        
    if res[13]:
        Display_forced_sub = '  /DISPLAYFORCEDSUB ' + '"' + res[13] + '"'   
    else:
        Display_forced_sub = ''
        
    if res[14]: 
        Jump_menu = '  /JUMPMENU ' + '"' + res[14] + '"'  
    else:
        Jump_menu = ''  
        
    if res[15]:
        Jump_main = '  /JUMPMAIN ' + '"' + res[15] + '"'    
    else:
        Jump_main = ''
        
    if res[16]:
        Out_disc = '  /OUTDISC ' + '"' + res[16] + '"'    
    else:
        Out_disc = ''
        
    if res[17]:
        Path_player = '  /PATHPLAYER ' + '"' + res[17] + '"'    
    else:
        Path_player = ''
        
    if res[18]:
        Preserve_menu_disc2 = '  /PRESERVEMENUDISC2 ' + '"' + res[18] + '"'   
    else:
        Preserve_menu_disc2 = '' 
        
    if res[19]:
        Profile = '  /PROFILE ' + '"' + res[19] + '"'
    else:
        Profile = ''
        
    if res[20]:
        Remove_DTS = '  /REMOVEDTS ' + '"' + res[20] + '"'   
    else:
        Remove_DTS = '' 
       
    if res[21]:
        Remove_HD_audio = '  /REMOVEHDAUDIO ' + '"' + res[21] + '"'   
    else:
        Remove_HD_audio = '' 
        
    if res[22]:
        Remove_menu = '  /REMOVEMENU ' + '"' + res[22] + '"'   
    else:
        Remove_menu = '' 
        
    if res[23]:
        Remove_PGC = '  /REMOVEPGC ' + '"' + res[23] + '"'   
    else:
        Remove_PGC = ''
    if res[24]:
        Rewind = '  /REWIND ' + '"' + res[24] + '"'
    else:
        Rewind = ''
        
    if res[25]:
        Subtitle = '  /SUBTITLE ' + '"' + res[25] + '"'    
    else:
        Subtitle = ''
        
    if res[26]:
        Title = '  /TITLE ' + '"' + res[26] + '"'    
    else: 
        Title = ''
        
    if res[27]:
        Volume = '  /VOLUME ' + '"' + res[27] + '"'  
    else:
        Volume = ''  
    
    if res[44]:    
        BD3DT = ' /BD3DCONVERTTYPE ' + '"' + res[44] + '"'
    else:
        BD3DT = ''

    if res[45]:
        COMPRESSTOAC3 = '/COMPRESSTOAC3 ' + '"' + res[45] + '"'
    else:
        COMPRESSTOAC3 = ''
    Close = '  /CLOSE'    
    Createminiso = '  /CREATEMINISO'
    if os.name == 'nt':
        cmd_string = Mode + Src + Dest + Audio + Audio_type + Change_play_order + Copy_IFO + Display_forced_sub + Jump_menu + Jump_main + Out_disc + Path_player \
                     + Preserve_menu_disc2 + Profile + Remove_DTS + Remove_HD_audio + Remove_menu + Remove_PGC + Rewind + Subtitle + Title + Volume + BD3DT + COMPRESSTOAC3 + Close + Createminiso
    else:
        cmd_string = Mode + Src + Dest + Audio + Audio_type + Change_play_order + Copy_IFO + Display_forced_sub + Jump_menu + Jump_main + Out_disc + Path_player \
                     + Preserve_menu_disc2 + Profile + Remove_DTS + Remove_HD_audio + Remove_menu + Remove_PGC + Rewind + Subtitle + Title + Volume + BD3DT + COMPRESSTOAC3 + Close
    
    return cmd_string, dest_path


def get_Filesize(dest_path):     
    Folder_size = 0  
    for root, _, all_files in os.walk(dest_path):                    
        for filespath in all_files:                     
            path_file = os.path.join(root, filespath)                           
            file_size = os.path.getsize(path_file)                        
            Folder_size += file_size     

    return Folder_size


def judge_filesize(res, Folder_size):    
    Folder_size = int(Folder_size.split('.')[0])
    result = ''
    if res[3].upper() == 'BD' and res[4].upper() == 'FULLDISC':
        if res[16].upper().startswith('BD50'):
            if Folder_size < 18000:
                result = 'folder_size too small; '
                initlog(result)
            elif Folder_size > 46100:
                result = 'folder_size too big; '
                initlog(result)
            else:
                initlog('the bd50 folder_size is normal; ')
        
        elif res[16].upper().startswith('BD25'):       
            if Folder_size < 15000:
                result = 'folder_size too small; '
                initlog(result)
            elif Folder_size > 23000:
                result = 'folder_size too big; '
                initlog(result)
            else:
                initlog('the bd25 folder_size is normal; ')
        
        elif res[16].upper().startswith('BD9'):        
            if Folder_size < 4000:
                result = 'folder_size too small; '  
                initlog(result) 
            elif Folder_size > 8100:
                result = 'folder_size too big; '
                initlog(result)
            else:
                initlog('the bd9 folder_size is normal; ')
        
        elif res[16].upper().startswith('BD5'):     
            if Folder_size < 2000:
                result = 'folder_size too small; '  
                initlog(result)
            elif Folder_size > 4300:
                result = 'folder_size too big; '
                initlog(result)
            else:
                initlog('the bd5 folder_size is normal; ')
        else:
            pass
        
    elif res[3].upper() == 'DVD' and res[4].upper() == 'FULLDISC' or res[3].upper() == 'BD' and res[4].upper() == 'BLURAYDVD':
        if res[16].upper().startswith('DVD5'):
            if Folder_size < 2000:
                result = 'folder_size too small; '
                initlog(result)
            elif Folder_size > 4300:
                result = 'folder_size too big; '
                initlog(result)
            else:
                initlog('the dvd5 folder_size is normal; ')
        elif res[16].upper().startswith('DVD9'):
            if Folder_size < 4000:
                result = 'folder_size too small; '
                initlog(result)
            elif Folder_size > 8100:
                result = 'folder_size too big; '
                initlog(result)
            else:
                initlog('the dvd9 folder_size is normal; ')
                   
    return result
           

def update_registry(path, valuename, value):
    import _winreg
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, path,  0, _winreg.KEY_ALL_ACCESS)    
    try:
        _winreg.SetValueEx(key, valuename, 0, _winreg.REG_DWORD, value)      
    except Exception, e:
        initlog('failed to update registry; ' + str(e))
  
  
def initlog(info):     
    #logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s - %(levelname)s: %(message)s') 
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 
    
    
def check_process_exist(process_name):    
    returncode = ''   
    try:
        p=os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name) 
        returncode = p.read().count(process_name)   
    except Exception, e:
        initlog(str(e))
    else:
        if returncode:
            initlog(process_name + ' exists')    
    return returncode


def kill_process(process_name): 
    try: 
        os.system('taskkill /f /im ' + process_name)        
    except Exception, e:
        initlog('failed to kill process; ' + str(e))      
    else:    
        initlog(process_name +' is killed now')  
        
        
def catch_all_picture(picture_path, index):     
    initlog('picure_path: ' + picture_path)
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S')   
    if os.name == 'nt':
        import ImageGrab
        try:       
            pic = ImageGrab.grab()
            pic.save(picture_path + '/' + str(index) + '-' + current_time + '.png')
            initlog('success to catch the picture')
        except Exception, e:
            initlog('failed to catch the picture; ' + str(e))
    else:
        try:
            os.system('screencapture ' +  picture_path + '/' + str(index) + '-' + current_time + '.png')
            initlog('success to catch the picture')
        except Exception, e:
            initlog('failed to catch the picture; ' + str(e))
            

def read_ini(ini_file):    
    project = ''
    bd_analysis_time = ''
    bd_interval_time = '' 
    bd_ripper_analysis_time = ''
    bd_ripper_interval_time = ''    
    dvd_analysis_time = ''  
    dvd_interval_time = ''
    file_analysis_time = ''  
    file_interval_time = ''
    bd_path = ''
    dvd_path = ''
    file_path = ''
    bd_path_mac = ''
    dvd_path_mac = ''
    file_path_mac = ''
    
    if os.path.exists(ini_file):
        try:    
            file(ini_file, 'r')
        except Exception, e:
            initlog('failed to open ini file!  ' + str(e)) 
            
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(ini_file))
        except Exception, e:
            initlog('failed to read ini file; ' + str(e))      
        else:    
            try:
                project = (config.get('Project', 'project')) 
                bd_analysis_time = int(config.get('BD/3Dcopy','analysis time')) 
                bd_interval_time = int(config.get('BD/3Dcopy','interval time')) 
                bd_ripper_analysis_time = int(config.get('BD/3Dcopy','ripper analysis time')) 
                bd_ripper_interval_time = int(config.get('BD/3Dcopy','ripper interval time')) 				
                dvd_analysis_time = int(config.get('DVD/DVDcopy','analysis time'))        
                dvd_interval_time = int(config.get('DVD/DVDcopy','interval time'))
                file_analysis_time = int(config.get('FILE','analysis time'))        
                file_interval_time = int(config.get('FILE','interval time'))
                bd_path = config.get('BD/3Dcopy','bd_path')
                dvd_path = config.get('DVD/DVDcopy', 'dvd_path')
                file_path = config.get('FILE','file_path')
                bd_path_mac = config.get('BD/3Dcopy','bd_path_mac')
                dvd_path_mac = config.get('DVD/DVDcopy', 'dvd_path_mac')
                file_path_mac = config.get('FILE','file_path_mac')
            except Exception, e:
                initlog('read ini file error; ' + str(e))
    else:
        initlog('dvdfab_auto_tool.ini file does not exist')
    return project, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time, dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac
    

def update_registry_value(res, project):    
    if not res[28]:
        Video_decoder_H264 = 0      
    else:
        Video_decoder_H264 = int(res[28])
        
    if not res[29]:
        Video_decoder_VC1 = 0
    else:   
        Video_decoder_VC1 = int(res[29])
    
    if not res[30]:
        Video_decoder_MPEG2  = 0      
    else: 
        Video_decoder_MPEG2 = int(res[30])
        
    if not res[31]:
        Video_encoder_H264 = 0
    else:
        Video_encoder_H264 = int(res[31])
        
    if Video_decoder_H264 == 1 or Video_decoder_VC1 == 1 or Video_decoder_MPEG2 == 1:        
        enableGPUA = 1        
    else:      
        enableGPUA = 0
    if os.name == 'nt':
        #XML_FILE = windows_xml.XML_FILE_PATH
        XML_FILE = get_new_file_ctime_windows(windows_xml.XML_FILE_PATH)
        if XML_FILE == '':
            return
        initlog('\ncurrent xml file is: ' +  XML_FILE)
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':  
            path_list = ["common_setting/FileMover","common_setting/BluRayToBluRay","common_setting/Generic","common_setting/DVD"]
            update_key_value_list = [('ShowWelcome', '0'),('EnableFileMover', '0'),('BDAVCHDCompatibility', '1'),('H264DecodeTypeUser_qt', '1'),('VC1DecodeTypeUser_qt', '1'),('Mpeg2DecodeTypeUser_qt', '1'),\
                                    ('EnableCudaEncodingUser_qt', '1'),('EnableDirectTranscoderUser_qt', '1'),('H264DecodeType_qt', str(Video_decoder_H264)),('VC1DecodeType_qt', str(Video_decoder_VC1)),\
                                    ('Mpeg2DecodeType_qt', str(Video_decoder_MPEG2)),('EnableCudaEncoding_qt', str(Video_encoder_H264)),('EnableGPUAccelerate_qt', str(enableGPUA)),('NotShowSetBDRegion', '1'),\
                                    ('AskOveride', '0')] 
            for path in path_list:
                try:
                    tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
                except Exception, e:
                    initlog(path + ' does not exist; ' + str(e))
                else:
                    for record in update_key_value_list:
                        if nodes[0].attrib.has_key(record[0]):
                            windows_xml.update_xml(nodes, record[0], record[1]) 
                    windows_xml.write_xml(tree, XML_FILE)
        else:
            path_list = ["common_setting/FileMover","common_setting/BluRayToBluRay","common_setting/Generic","common_setting/DVD"]
            update_key_value_list = [('ShowWelcome', '0'),('EnableFileMover', '0'),('BDAVCHDCompatibility', '1'),('H264DecodeTypeUser_qt', '1'),('VC1DecodeTypeUser_qt', '1'),('Mpeg2DecodeTypeUser_qt', '1'),\
                                    ('EnableCudaEncodingUser_qt', '1'),('EnableDirectTranscoderUser_qt', '1'),('H264DecodeType_qt', str(Video_decoder_H264)),('VC1DecodeType_qt', str(Video_decoder_VC1)),\
                                    ('Mpeg2DecodeType_qt', str(Video_decoder_MPEG2)),('EnableCudaEncoding_qt', str(Video_encoder_H264)),('EnableDirectTranscoder_qt', str(enableGPUA)),('NotShowSetBDRegion', '1'),\
                                    ('AskOveride', '0')] 
            for path in path_list:
                try:
                    tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
                except Exception, e:
                    initlog(path + ' does not exist; ' + str(e))
                else:
                    for record in update_key_value_list:
                        if nodes[0].attrib.has_key(record[0]):
                            windows_xml.update_xml(nodes, record[0], record[1]) 
                    windows_xml.write_xml(tree, XML_FILE)     
        
        """
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':   
            update_registry_list = [('Software\\DVDFab\\V8_QT\\FileMover\\', 'EnableFileMover', 0), ('Software\\DVDFab\\V8_QT\\BluRayToBluRay\\', 'BDAVCHDCompatibility', 1), \
                            ('Software\\DVDFab\\V8_QT\\Generic\\', 'H264DecodeTypeUser_qt', 1), ('Software\\DVDFab\\V8_QT\\Generic\\', 'VC1DecodeTypeUser_qt', 1),\
                            ('Software\\DVDFab\\V8_QT\\Generic\\', 'Mpeg2DecodeTypeUser_qt', 1), ('Software\\DVDFab\\V8_QT\\Generic\\', 'EnableCudaEncodingUser_qt', 1),\
                            ('Software\\DVDFab\\V8_QT\\Generic\\', 'EnableDirectTranscoderUser_qt', 1), ("Software\\DVDFab\\V8_QT\\Generic\\", 'H264DecodeType_qt', Video_decoder_H264),\
                            ("Software\\DVDFab\\V8_QT\\Generic\\", 'VC1DecodeType_qt', Video_decoder_VC1), ("Software\\DVDFab\\V8_QT\\Generic\\", 'Mpeg2DecodeType_qt', Video_decoder_MPEG2),\
                            ("Software\\DVDFab\\V8_QT\\Generic\\", 'EnableCudaEncoding_qt', Video_encoder_H264), ("Software\\DVDFab\\V8_QT\\Generic\\", 'EnableGPUAccelerate_qt', enableGPUA),\
                            ('Software\\DVDFab\\V8_QT\\DVD\\', 'NotShowSetBDRegion', 1), ('Software\\DVDFab\\V8_QT\\Generic\\', 'AskOveride', 0)] 
        else:
            update_registry_list = [('Software\\DVDFab\\V9\\FileMover\\', 'EnableFileMover', 0), ('Software\\DVDFab\\V9\\BluRayToBluRay\\', 'BDAVCHDCompatibility', 1), \
                            ('Software\\DVDFab\\V9\\Generic\\', 'H264DecodeTypeUser_qt', 1), ('Software\\DVDFab\\V9\\Generic\\', 'VC1DecodeTypeUser_qt', 1),\
                            ('Software\\DVDFab\\V9\\Generic\\', 'Mpeg2DecodeTypeUser_qt', 1), ('Software\\DVDFab\\V9\\Generic\\', 'EnableCudaEncodingUser_qt', 1),\
                            ('Software\\DVDFab\\V9\\Generic\\', 'EnableDirectTranscoderUser_qt', 1), ("Software\\DVDFab\\V9\\Generic\\", 'H264DecodeType_qt', Video_decoder_H264),\
                            ("Software\\DVDFab\\V9\\Generic\\", 'VC1DecodeType_qt', Video_decoder_VC1), ("Software\\DVDFab\\V9\\Generic\\", 'Mpeg2DecodeType_qt', Video_decoder_MPEG2),\
                            ("Software\\DVDFab\\V9\\Generic\\", 'EnableCudaEncoding_qt', Video_encoder_H264), ("Software\\DVDFab\\V9\\Generic\\", "EnableDirectTranscoder_qt", 0),\
                            ('Software\\DVDFab\\V9\\DVD\\', 'NotShowSetBDRegion', 1), ('Software\\DVDFab\\V9\\Generic\\', 'AskOveride', 0)]
        try:
            for record in update_registry_list:           
                update_registry(record[0], record[1], record[2])            
        except Exception, e:
            initlog('fail to update registry value; ' + str(e))
            
        """        
    else:
        #XML_FILE = get_ctime(myxml.XML_FILE_PATH)
        XML_FILE = get_new_file_ctime_macos(myxml.XML_FILE_PATH)
        if XML_FILE == '':
            return
        initlog('\ncurrent xml file is: ' +  XML_FILE)
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':  
            path_list = ["common_setting/FileMover","common_setting/BluRayToBluRay","common_setting/Generic","common_setting/DVD"]
            update_key_value_list = [('ShowWelcome', '0'),('EnableFileMover', '0'),('BDAVCHDCompatibility', '1'),('H264DecodeTypeUser_qt', '1'),('VC1DecodeTypeUser_qt', '1'),('Mpeg2DecodeTypeUser_qt', '1'),\
									('EnableCudaEncodingUser_qt', '1'),('EnableDirectTranscoderUser_qt', '1'),('H264DecodeType_qt', str(Video_decoder_H264)),('VC1DecodeType_qt', str(Video_decoder_VC1)),\
									('Mpeg2DecodeType_qt', str(Video_decoder_MPEG2)),('EnableCudaEncoding_qt', str(Video_encoder_H264)),('EnableGPUAccelerate_qt', str(enableGPUA)),('NotShowSetBDRegion', '1'),\
									('AskOveride', '0')] 
            for path in path_list:
                try:
                    tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp)  
                except Exception, e:
                    initlog(path + ' does not exist; ' + str(e))
                else:
                    for record in update_key_value_list:
                        if nodes[0].attrib.has_key(record[0]):
                            myxml.update_xml(nodes, record[0], record[1]) 
                    myxml.write_xml(tree, XML_FILE)
        else:
            path_list = ["common_setting/FileMover","common_setting/BluRayToBluRay","common_setting/Generic","common_setting/DVD"]
            update_key_value_list = [('ShowWelcome','0'),('EnableFileMover', '0'),('BDAVCHDCompatibility', '1'),('H264DecodeTypeUser_qt', '1'),('VC1DecodeTypeUser_qt', '1'),('Mpeg2DecodeTypeUser_qt', '1'),\
									('EnableCudaEncodingUser_qt', '1'),('EnableDirectTranscoderUser_qt', '1'),('H264DecodeType_qt', str(Video_decoder_H264)),('VC1DecodeType_qt', str(Video_decoder_VC1)),\
									('Mpeg2DecodeType_qt', str(Video_decoder_MPEG2)),('EnableCudaEncoding_qt', str(Video_encoder_H264)),('EnableDirectTranscoder_qt', str(enableGPUA)),('NotShowSetBDRegion', '1'),\
									('AskOveride', '0')] 
            for path in path_list:
                try:
                    tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp)  
                except Exception, e:
                    initlog(path + ' does not exist; ' + str(e))
                else:
                    for record in update_key_value_list:
                        if nodes[0].attrib.has_key(record[0]):
                            myxml.update_xml(nodes, record[0], record[1]) 
                    myxml.write_xml(tree, XML_FILE)
 
    
def remove_fab_logfile(fab_logpath):
    if os.path.exists(fab_logpath):
        files = os.listdir(fab_logpath)    
        for onefile in files:        
            path_file = os.path.join(fab_logpath, onefile)        
            try:
                os.remove(path_file)   
                initlog("remove fab log files successfully")				
            except Exception, e:
                initlog('fail to remove log files; ' + str(e))
    else:
        initlog('cannot remove fab logfiles, log and temp do not exist')  
               
            
def get_log_files(logpath):    
    log_filename_list = []
    if logpath:
        for path in logpath:  
            for root, _, files in os.walk(path):                
                for onefile in files: 
                    if os.path.splitext(onefile)[1].lower()  == '.bin' or os.path.join(root, onefile).find("BDMV") != -1:      
                        continue   
                    else:  
                        path_file = os.path.join(root, onefile)           
                        log_filename_list.append(path_file)
                        initlog("log_filename_list: " + str(log_filename_list))
    else:
        initlog('cannot get logfiles, log and temp do not exist')    
    return log_filename_list


def copy_file(log_filename_list, dest_path):  
    for src_file in log_filename_list:
        if os.path.isfile(src_file): 
            if os.path.isdir(dest_path):      
                pass
            else:
                os.makedirs(dest_path)
            errors = []                             
            srcname = src_file    
            filename = os.path.basename(src_file)
            dstname = os.path.join(dest_path, filename)   
            try:                                
                if os.path.isfile(srcname):        
                    copy2(srcname, dstname) 
                elif os.path.isdir(dstname):          
                    os.remove(dstname)
                    copy2(srcname, dstname)    
            except Exception, e:
                initlog(str(e))
                      
            try:                               
                copystat(srcname, dstname)              
            except Exception, e:
                initlog(str(e))
            if errors:                          
                raise Error(errors)             
        else:
            initlog('the fisrt parm should be a file name')

    
def zip_files(log_filename_list,zipfilename):    
    initlog("zip files log_filename_list: " + str(log_filename_list))
    if log_filename_list:
        zf = zipfile.ZipFile(zipfilename, 'a', zipfile.zlib.DEFLATED)      
        for log_filename in log_filename_list:     
            try:
                if '/TEMP/' in log_filename.upper() or '\\TEMP\\' in log_filename.upper():
                    zf.write(log_filename, "temp" + os.sep  + os.path.split(log_filename)[1], zipfile.ZIP_DEFLATED)
                else:
                    zf.write(log_filename, "log" + os.sep + os.path.split(log_filename)[1], zipfile.ZIP_DEFLATED)        
            except Exception, e:
                initlog('failed to zip files; ' + str(e))                
        zf.close()
        
    else:
        initlog('log and temp to be ziped does not exist\n')
                       

def upload_file(log_filename_list, index):  
    initlog("begin to upload files to server!!!!!!!")  
    for filename in log_filename_list:
        ftp_server = '10.10.2.11'
        ftp_port = '21'
        remotepath = '.'
        
        ftp = FTP()  
        ftp.set_debuglevel(2)
        ftp.connect(ftp_server, ftp_port)
        ftp.login('', '')
        ftp.cwd(remotepath)
        bufsize = 1024
        
        try:
            file_handler = open(filename, 'rb')  
            ftp.storbinary('STOR %s' % (str(index) + '_' + os.path.basename(filename)), file_handler, bufsize)
            ftp.set_debuglevel(0)
        except Exception, e:
            initlog('failed to upload files; ' + str(e))
        else:
            file_handler.close()
        finally:
            ftp.quit()


def get_picture_path(res):
    if '.ISO' == os.path.splitext(res[6].upper())[1]: 
        picture_path = os.path.split(res[6])[0]  
    else:
        picture_path = res[6]
    picture_path = change_fuhao(picture_path)
    return picture_path

    
def start_running(res, DVDFab_path_cmd_string, module, ripper_mode, dest_path, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time,dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, burn_engine_type, client_dest_path):    
    result = ''
    try:       
        initlog('now, DVDFab starts running')
        if os.name == 'nt':
            p = subprocess.Popen(DVDFab_path_cmd_string) 
            #time.sleep(60)
            #subprocess.call(CLICK_OK)
        else:
            p = subprocess.Popen(DVDFab_path_cmd_string, shell = True)  
        #time.sleep(35)
        #try:
        #    subprocess.Popen(CLICK_TRY)
        #except Exception, e:
        #    initlog(str(e) + ' failed to click the try button;')
    except Exception, e:
        initlog('DVDFab failed to run; ' + str(e))      
        result = 'Fab does not run; '
        initlog(result)
    else: 
        if module == 'BD': 
            if ripper_mode.upper() == "RIPPER":
                initlog("this case is ripper")
                bd_analysis_time = bd_ripper_analysis_time	
                bd_interval_time = bd_ripper_interval_time
            else:
                pass			
            initlog('the bd_analysis_time is beginning')
            initlog("the bd_analysis_time is: " + str(bd_analysis_time) + " mins")
            for i in range(bd_analysis_time):                
                if p.poll() is None:                    
                    time.sleep(60)              
                else:  
                    if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                        dest_path1 = os.path.split(res[6])[0]
                    else:
                        dest_path1 = res[6]
                    dest_path1 = change_fuhao(dest_path1)
                    if not os.path.exists(dest_path1):
                        try:
                            os.makedirs(dest_path1)
                        except Exception, e:
                            initlog('failed to create Folder path; ' + str(e))
                        else:
                            dest_path1 = change_fuhao(dest_path1)
                            catch_all_picture(dest_path1, res[0])
                            initlog('Folder path created by me; ')   
                    else:
                        catch_all_picture(dest_path1, res[0])                     
                    result = 'Fab killed in the beginning; '                 
                    initlog(result)                
                    return  result   
            initlog('the bd_analysis_time is over')                                                                      
            flag = 1            
            number = 0                        
            while flag:
                if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                    dest_path1 = os.path.split(res[6])[0]
                else:
                    dest_path1 = res[6]
                dest_path1 = change_fuhao(dest_path1)
                if not os.path.exists(dest_path1):
                    try:
                        os.makedirs(dest_path1)
                    except Exception, e:
                        initlog('failed to create Folder path; ' + str(e))
                    else:
                        dest_path1 = change_fuhao(dest_path1)
                        catch_all_picture(dest_path1, res[0])
                        initlog('Folder path created by me; ')
                    break 
                First_size = get_Filesize(dest_path)        
                initlog('First_size: ' + str(First_size))
                flag = 0        
                number += bd_interval_time * 30                                                          
                if p.poll() is None:                   
                    flag = 1            
                    time.sleep(bd_interval_time * 30)                    
                    if number == bd_interval_time * 60:                        
                        number = 0 
                        Last_size = get_Filesize(dest_path) 
                        initlog('Last_size: ' + str(Last_size))
                        if Last_size - First_size <= 0:
                            flag = 0    
                            time.sleep(120)
                            if p.poll() is None:
                                if '.ISO' == os.path.splitext(res[6].upper())[1]:
                                    tempfolder_to_iso(burn_engine_type, res[6])
                                else:
                                    initlog('*****DVDFab still exists')   
                                    picture_path = get_picture_path(res) 
                                    if p.poll() is None:                                                                                             
                                        catch_all_picture(picture_path, res[0])   
                                        if result == '':                       
                                            result = 'Freeze and cancel dvdfab; '     
                                        initlog(result)
                                        try:
                                            subprocess.call(TESTBAT_PATH)
                                            initlog('DVDFab may killed by Sikuli')
                                        except Exception, e:
                                            initlog('DVDFab does not killed by Sikuli')   
                            else:
                                pass                     
                        else:  
                            pass                      
                                                  
        elif module == 'DVD':         
            initlog('the dvd_analysis_time is beginning')      
            for i in range(dvd_analysis_time):               
                if p.poll() is None:                    
                    time.sleep(60)                      
                else:   
                    if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                        dest_path1 = os.path.split(res[6])[0]
                    else:
                        dest_path1 = res[6]
                    dest_path1 = change_fuhao(dest_path1)
                    if not os.path.exists(dest_path1):
                        try:
                            os.makedirs(dest_path1)
                        except Exception, e:
                            initlog('failed to create Folder path; ' + str(e))
                        else:
                            dest_path1 = change_fuhao(dest_path1)
                            catch_all_picture(dest_path1, res[0])
                            initlog('Folder path created by me; ') 
                    else:
                        catch_all_picture(dest_path1, res[0])                  
                    result = 'Fab killed in the beginning; '             
                    initlog(result)                                    
                    return  result   
            initlog('the dvd_analysis_time is over')                                                                  
            flag = 1            
            number = 0                        
            while flag:                               
                if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                    dest_path1 = os.path.split(res[6])[0] 
                else:
                    dest_path1 = res[6]       
                dest_path1 = change_fuhao(dest_path1)
                if not os.path.exists(dest_path1):
                    try:
                        os.makedirs(dest_path1)
                    except Exception, e:
                        initlog('failed to create Folder path; ' + str(e))
                    else:
                        dest_path1 = change_fuhao(dest_path1)
                        catch_all_picture(dest_path1, res[0])
                        initlog('Folder path created by me; ')
                    break  
                First_size = get_Filesize(dest_path)       
                initlog('First_size: ' + str(First_size))            
                flag = 0                
                number += dvd_interval_time * 30                      
                if p.poll() is None:                 
                    flag = 1            
                    time.sleep(dvd_interval_time * 30)                    
                    if number == dvd_interval_time * 60:                        
                        number = 0 
                        Last_size = get_Filesize(dest_path)   
                        initlog('Last_size: ' + str(Last_size))                    
                        if Last_size - First_size <= 0:  
                            flag = 0  
                            time.sleep(120)
                            if p.poll() is None:
                                if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                                    tempfolder_to_iso(burn_engine_type, res[6]) 
                                else:         
                                    initlog('******DVDFab still exists')     
                                    picture_path = get_picture_path(res) 
                                    if p.poll() is None:                                                                                   
                                        catch_all_picture(picture_path, res[0])           
                                        if result == '':                 
                                            result = 'Freeze and cancel dvdfab; '
                                        initlog(result)
                                        try:
                                            subprocess.call(TESTBAT_PATH)
                                            initlog('DVDFab may canceled by Sikuli')
                                        except Exception, e:
                                            initlog('DVDFab does not canceled by Sikuli') 
                            else:
                                pass
                        else:    
                            pass 
                        
        else:         
            initlog('the file_analysis_time is beginning')    
            for i in range(file_analysis_time):               
                if p.poll() is None:                    
                    time.sleep(60)                      
                else:   
                    if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                        dest_path1 = os.path.split(res[6])[0]
                    else:
                        dest_path1 = res[6]
                    dest_path1 = change_fuhao(dest_path1)
                    if not os.path.exists(dest_path1):
                        try:
                            os.makedirs(dest_path1)
                        except Exception, e:
                            initlog('failed to create Folder path; ' + str(e))
                        else:
                            dest_path1 = change_fuhao(dest_path1)
                            catch_all_picture(dest_path1, res[0])
                            initlog('Folder path created by me; ') 
                    else:
                        catch_all_picture(dest_path1, res[0])                  
                    result = 'Fab killed in the beginning; '             
                    initlog(result)                                    
                    return  result   
            initlog('the file_analysis_time is over')                                                                  
            flag = 1            
            number = 0                        
            while flag:                               
                if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                    dest_path1 = os.path.split(res[6])[0] 
                else:
                    dest_path1 = res[6]    
                dest_path1 = change_fuhao(dest_path1)   
                if not os.path.exists(dest_path1):
                    try:
                        os.makedirs(dest_path1)
                    except Exception, e:
                        initlog('failed to create Folder path; ' + str(e))
                    else:
                        dest_path1 = change_fuhao(dest_path1)
                        catch_all_picture(dest_path1, res[0])
                        initlog('Folder path created by me; ')
                    break  
                First_size = get_Filesize(dest_path)       
                initlog('First_size: ' + str(First_size))            
                flag = 0                
                number += file_interval_time * 30                      
                if p.poll() is None:                 
                    flag = 1            
                    time.sleep(file_interval_time * 30)                    
                    if number == file_interval_time * 60:                        
                        number = 0 
                        Last_size = get_Filesize(dest_path)   
                        initlog('Last_size: ' + str(Last_size))                    
                        if Last_size - First_size <= 0:  
                            flag = 0  
                            time.sleep(120)
                            if p.poll() is None:
                                if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                                    tempfolder_to_iso(burn_engine_type, res[6]) 
                                else:         
                                    initlog('******DVDFab still exists')     
                                    picture_path = get_picture_path(res) 
                                    if p.poll() is None:                                                                                   
                                        catch_all_picture(picture_path, res[0])         
                                        if result == '':                 
                                            result = 'Freeze and cancel dvdfab; '
                                        initlog(result)
                                        try:
                                            subprocess.call(TESTBAT_PATH)
                                            initlog('DVDFab may canceled by Sikuli')
                                        except Exception, e:
                                            initlog('DVDFab does not canceled by Sikuli') 
                            else:
                                pass
                        else:    
                            pass                                                                                                                                
        return result
    

def tempfolder_to_iso(burn_engine_type, dest_path):   
    dest_path = change_fuhao(dest_path)
    initlog('tempfolder to iso is beginning!')
    dest_path = os.path.split(dest_path)[0]
    for i in range(6):      
        if not os.path.exists(dest_path):
            try:
                os.makedirs(dest_path)
            except Exception,e :
                initlog('failed to create Folder path; ' + str(e))
            else:
                result = 'Folder path created by me; '
                initlog(result + dest_path)
            break
        First_size = get_Filesize(dest_path)
        initlog('First_size: ' + str(First_size)) 
        time.sleep(600)
        Last_size = get_Filesize(dest_path)
        initlog('Last_size: ' + str(Last_size))
        if Last_size - First_size <= 0:
            break
    initlog('tempfolder to iso is over')
 

def before_running(res, src_iso_path, client_dest_path, DVDFab_path, project):
    cmd_string, dest_path = get_cmd_string(res, src_iso_path, client_dest_path) 
    DVDFab_path_cmd_string = DVDFab_path + cmd_string  
    initlog('THE RUNNING CASE ID: ' + str(res[0]))
    initlog('the cmd_string: ' + DVDFab_path_cmd_string)
    if os.name == 'nt':
        #XML_FILE = windows_xml.XML_FILE_PATH
        XML_FILE = get_new_file_ctime_windows(windows_xml.XML_FILE_PATH)
        if XML_FILE == '':
            return 
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':
            path_list = ["common_setting/Generic","common_setting/DVD"]
            for path in path_list:
                tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
                if nodes[0].attrib.has_key('LogFolder'):
                    fab_logpath = nodes[0].attrib['LogFolder']
                if nodes[0].attrib.has_key('BurnEngineType'):
                    burn_engine_type = nodes[0].attrib['BurnEngineType']
                if nodes[0].attrib.has_key('TempFolder'):
                    tempfolder_path = nodes[0].attrib['TempFolder']
        else:
            path_list = ["common_setting/Generic","common_setting/DVD"]
            for path in path_list:
                tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
                if nodes[0].attrib.has_key('LogFolder'):
                    fab_logpath = nodes[0].attrib['LogFolder']
                if nodes[0].attrib.has_key('BDBurnEngineType'):
                    burn_engine_type = nodes[0].attrib['BDBurnEngineType']
                if nodes[0].attrib.has_key('TempFolder'):
                    tempfolder_path = nodes[0].attrib['TempFolder']   
        
        """
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':
            fab_logpath = get_registry_value("Software\\DVDFab\\V8_QT\\Generic\\", "LogFolder")           
            burn_engine_type = get_registry_value("Software\\DVDFab\\V8_QT\\DVD\\", 'BurnEngineType')
            tempfolder_path = get_registry_value("Software\\DVDFab\\V8_QT\\Generic\\", 'TempFolder') 
        else:
            fab_logpath = get_registry_value("Software\\DVDFab\\V9\\Generic\\", "LogFolder")           
            burn_engine_type = get_registry_value("Software\\DVDFab\\V9\\DVD\\", 'BDBurnEngineType')
            tempfolder_path = get_registry_value("Software\\DVDFab\\V9\\Generic\\", 'TempFolder')  
        """
    else:
        #XML_FILE = get_ctime(myxml.XML_FILE_PATH)
        XML_FILE = get_new_file_ctime_macos(myxml.XML_FILE_PATH)
        if XML_FILE == '':
            return
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':
            path_list = ["common_setting/Generic","common_setting/DVD"]
            for path in path_list:
                tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp)  
                if nodes[0].attrib.has_key('LogFolder'):
                    fab_logpath = nodes[0].attrib['LogFolder']
                if nodes[0].attrib.has_key('BurnEngineType'):
                    burn_engine_type = nodes[0].attrib['BurnEngineType']
                if nodes[0].attrib.has_key('TempFolder'):
                    tempfolder_path = nodes[0].attrib['TempFolder']
        else:
            path_list = ["common_setting/Generic","common_setting/DVD"]
            for path in path_list:
                tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp)  
                if nodes[0].attrib.has_key('LogFolder'):
                    fab_logpath = nodes[0].attrib['LogFolder']
                if nodes[0].attrib.has_key('BDBurnEngineType'):
                    burn_engine_type = nodes[0].attrib['BDBurnEngineType']
                if nodes[0].attrib.has_key('TempFolder'):
                    tempfolder_path = nodes[0].attrib['TempFolder']                       
     
    if '.ISO' == os.path.splitext(res[6].upper())[1]:          
        dest_path = tempfolder_path
    initlog('before running, dest_path is: ' + dest_path)    
    tempfolder_path = ''.join((tempfolder_path, 'ReportCrash'))  
    fab_logpath = fab_logpath.replace("_nbsp;"," ")
    tempfolder_path = tempfolder_path.replace("_nbsp;"," ")
    initlog("fab_logpath is: " + fab_logpath)
    initlog("tempfolder_path is: " + tempfolder_path)
    logpath = (fab_logpath, tempfolder_path)         
    remove_fab_logfile(fab_logpath)
    return DVDFab_path_cmd_string, dest_path, logpath, burn_engine_type


def update_session_before_running(pc_name, src_iso_path, res):    
    #start = datetime.datetime.now()      
    #Start_time = str(start).split('.')[0]         
    start = time.mktime(time.localtime())
    Start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    src_iso_path = src_iso_path.replace('\\','\\\\')  
    update_flag = update_session_table(res, 1, res[0], res[1], pc_name, src_iso_path, Start_time) 
    return start, Start_time, src_iso_path, update_flag

  
def change_fuhao(file_path):
    if os.name == 'nt':
        file_path = file_path.replace('/','\\')
    else:
        file_path = file_path.replace('\\','/')
    return file_path
   

def after_running(dest_path, index):    
    result = ''
    process_list = ["DVDFab.exe", "WerFault.exe", "dwwin.exe", "FabReport.exe"]
    dest_path = change_fuhao(dest_path)
    if '.ISO' == os.path.splitext(dest_path.upper())[1]: 
        dest_path = os.path.split(dest_path)[0]
        
    for process_name in process_list:
        returncode = check_process_exist(process_name)                               
        if returncode:   
            initlog(' **has process exist** ') 
            try:
                catch_all_picture(dest_path, index)   
            except Exception, e:
                initlog('failed to catch picture; ' + str(e))   
            kill_process(process_name)
            result += process_name + ' killed; '
    if result == '':
        initlog('after running result: no process exists')
    else:        
        initlog('after_running result:  ' + result)
    return result


def after_running_on_macos(dest_path, index):
    result = ''
    dest_path = change_fuhao(dest_path)
    if '.ISO' == os.path.splitext(dest_path.upper())[1]: 
        dest_path = os.path.split(dest_path)[0]
    process_list = ['DVDFab']
    for process_name in process_list:
        txt = check_process(process_name)
        if '/Applications/DVDFab 9.app/Contents/MacOS/DVDFab' in txt: 
            initlog('**has process exist** ')
            try:
                catch_all_picture(dest_path, index)   
            except Exception, e:
                initlog('failed to catch picture; ' + str(e)) 
            kill_process_name(process_name)
            result += process_name + ' killed; '
        else:
            initlog('no process exists; ')
    if result == '':
        initlog('after running result: no process exists')
    else:        
        initlog('after_running result:  ' + result)
    return result


def check_process(process_name):
    cmd = 'ps -ef | grep %s' % process_name
    f = os.popen(cmd)
    regex = re.compile(r'\w+\s+(\d+)\s+.*')
    txt = f.read()
    return  txt
    
    
def kill_process_name(process_name):
    os.system('killall ' + process_name)


def update_session_after_running(pc_name, res, start, Start_time, src_iso_path, result):    
    dest_path = change_fuhao(res[6])
    if '.ISO' == os.path.splitext(dest_path.upper())[1]: 
        dest_path = os.path.split(dest_path)[0]
    end = time.mktime(time.localtime())
    End_time = time.strftime('%Y-%m-%d %H:%M:%S')
    Total_time = str(end-start).split('.')[0]
    Total_time = int(Total_time)
    Total_time = str(Total_time/3600)+':'+str(Total_time%3600/60)+':'+str(Total_time%3600%60%60)
    #end = datetime.datetime.now()    
    #End_time = str(end).split('.')[0]    
    #Total_time = (end - start).seconds    
    #Total_time = str(Total_time/3600)+':'+str(Total_time%3600/60)+':'+str(Total_time%3600%60%60)           
    Folder_size = get_Filesize(dest_path)  
    Folder_size = Folder_size/1024.0/1024.0
    Folder_size = '%.2lf' % Folder_size
    initlog('the terminal Folder_size: ' + str(Folder_size))
    if result != '':
        initlog(result)
    result1 = judge_filesize(res, Folder_size) 
    if result is None or result == '':
        result = result1
    else:
        result += result1
    initlog('after running, after Folder_size, the dest_path is: ' + dest_path)
    if result == '':
        update_flag = update_session_table(res, 2, res[0], res[1], pc_name, src_iso_path, Start_time, End_time, Total_time, Folder_size, result)
    else:
        update_flag = update_session_table(res, 3, res[0], res[1], pc_name, src_iso_path, Start_time, End_time, Total_time, Folder_size, result)
    return update_flag
    
    
def running(pc_name, res, client_dest_path, DVDFab_path, project, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time,dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac):     
    start = ''
    Start_time = ''
    dest_path = ''
    result = ''
    logpath = ''
    burn_engine_type = ''
    update_registry_value(res, project)          
    module, iso,ripper_mode = res_to_iso(res)       
    src_iso_path = search_iso_path(module, iso, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac)  
    update_flag = False      
    
    if src_iso_path:  
        DVDFab_path_cmd_string, dest_path, logpath, burn_engine_type = before_running(res, src_iso_path, client_dest_path, DVDFab_path, project)
        start, Start_time, src_iso_path, update_flag = update_session_before_running(pc_name, src_iso_path, res) 
        if update_flag:
            initlog('the session table update before running')
        else:
            result = ' Auto_test_tool raise error;'
            update_session_table(res, 2, res[0], res[1], pc_name, src_iso_path = '', Start_time = '', End_time = '', Total_time = '', Folder_size = '', result = result)    #Auto_test_tool
            initlog('Auto_test_tool raise error')  
            return  start, Start_time, dest_path, src_iso_path, result, logpath, burn_engine_type, update_flag       
        result = start_running(res, DVDFab_path_cmd_string, module, ripper_mode, dest_path, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time,dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, burn_engine_type, client_dest_path)      
    else:
        result = 'does not find iso; '
        initlog(result)
        
    return start, Start_time, dest_path, src_iso_path, result, logpath, burn_engine_type, update_flag

 
commands = {"Darwin" : {"ipv4":"ifconfig | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{print $2}'", 
                    "ipv6": "ifconfig | grep -E 'inet6.[0-9]' | grep -v 'fe80:' | awk '{print $2}'"},
            "Linux" : {"ipv4": "sbin/ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}'",
                "ipv6": "/sbin/ifconfig | grep 'inet6 addr:' | grep 'Global' | grep -v 'fe80 | awk '{print $3}'"}
            }

def ip_address(version):
    proc = subprocess.Popen(commands[platform.system()][version], shell=True, stdout=subprocess.PIPE)
    return proc.communicate()[0].replace('\n', ';')


def ipv6_address():
    if os.name == "nt":
        return socket.gethostbyname(socket.gethostname())
    else:
        return ip_address('ipv6').split(";")[0]


def ipv4_address():
    if os.name == "nt":
        return socket.gethostbyname(socket.gethostname())
    else:
        return ip_address('ipv4').split(";")[0]
   

def get_new_file_ctime_macos(path):
    file_list = []
    ctime_list = []
    file_ctime_list = []
    fab_config_file_list = []
    for onefile in os.listdir(path):
        if onefile.upper().startswith('CONFIG'):
            path_file= os.path.join(path, onefile)
            if os.path.isdir(path_file):
                file_list.append(path_file)
                st = os.stat(path_file)
                ctime_list.append(st.st_ctime)

    XML_FILES = os.listdir(file_list[ctime_list.index(max(ctime_list))])
    if XML_FILES != []:
        for file in XML_FILES:
            file_path = os.path.join(file_list[ctime_list.index(max(ctime_list))], file)
            fab_config_file_list.append(file_path)
            file_ctime_list.append(os.stat(file_path).st_ctime)
        XML_FILE = fab_config_file_list[file_ctime_list.index(max(file_ctime_list))]
    else:
        XML_FILE = ''
    return XML_FILE


def get_new_file_ctime_windows(path):
    file_list = []
    ctime_list = []
    for onefile in os.listdir(path):  
        if onefile.upper().startswith('FAB_CONFIG'):
            path_file= os.path.join(path, onefile)
            if os.path.isfile(path_file):
                file_list.append(path_file)
                st = os.stat(path_file)
                ctime_list.append(st.st_ctime)
    if ctime_list == []:
        XML_FILE = ''
    else:
        XML_FILE = file_list[ctime_list.index(max(ctime_list))]
    return XML_FILE
   
   
def main(): 
    initlog('current_path: ' + current_path)  
    
    pc_name = get_pcname()   
    if os.name == 'nt':
        client_ip, client_dest_path = get_ip_address(pc_name)  
    else:       
        pc_ip = ipv4_address()
        pc_name, client_dest_path = get_client_path(pc_ip)
    dest_path = change_fuhao(client_dest_path)
    """
    if os.name == 'nt':
        
        XML_FILE = get_new_file_ctime_windows(windows_xml.XML_FILE_PATH)
        if XML_FILE == '':
            return
        tree, nodes = windows_xml.read_xml(XML_FILE, 'common_setting/Generic', xml_temp)
        try:
            DVDFab_path = nodes[0].attrib['Path']
            #DVDFab_path = DVDFab_path.replace('_nbsp;',' ')
        except Exception, e:
            initlog('does not find DVDFab path; ' + str(e))
        p = subprocess.Popen(DVDFab_path) 
        time.sleep(20)
        subprocess.call(KILL_DVDFAB_PATH)
        time.sleep(30)
        #kill_process('DVDFab.exe')
    else:
        DVDFab_path = DVDFAB_PATH
        #p = subprocess.Popen(DVDFAB_PATH, shell = True)  
        #time.sleep(25)
        #kill_process_name('DVDFab')
    """    
    while 1:     
        res = search_session_table(pc_name)

        if not res:        
            initlog('sorry , does not have any case for you;\n')        
            return 
        
        project, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time,dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac = read_ini(INI_FILE) 
        """
        if os.name == 'nt':
            #DVDFab_path = DVDFab_path
            if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':
                DVDFab_path = get_registry_value("Software\\DVDFab\\V8_QT", 'Path')   
            else:
                DVDFab_path = get_registry_value("Software\\DVDFab\\V9", 'Path') 
            
        else:
            DVDFab_path = DVDFAB_PATH
        """        
        if os.name == 'nt': 
            XML_FILE = get_new_file_ctime_windows(windows_xml.XML_FILE_PATH)
            if XML_FILE == '':
                initlog("xudedong ,does not find %s" % XML_FILE)
                return
            #change it at 2013-09-16
            #windows_xml.delete(XML_FILE, windows_xml.xml_temp)
            tree, nodes = windows_xml.read_xml(XML_FILE, 'common_setting', xml_temp)
            
            try:
                DVDFab_path = nodes[0].attrib['Path']
                initlog("find DVDFab path: %s" % DVDFab_path)
                #DVDFab_path = DVDFab_path.replace('_nbsp;',' ')
            except Exception, e:
                DVDFab_path = ""
                initlog('does not find DVDFab path; xml file analyze error;' + str(e))
        else:
            DVDFab_path = DVDFAB_PATH

        if DVDFab_path:   
            start,Start_time,dest_path,src_iso_path,result,logpath,burn_engine_type, update_flag = running(pc_name,res,client_dest_path,DVDFab_path,project,bd_analysis_time,bd_interval_time,bd_ripper_analysis_time, bd_ripper_interval_time,dvd_analysis_time,dvd_interval_time, file_analysis_time, file_interval_time, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac) 
            
            if start == '' or update_flag == False: 
                update_session_table(res, 2, res[0], res[1], pc_name, result = result)       #does not find iso;
                initlog('the session table does not update before running\n')             
            else:
                if os.name == 'nt':           
                    result1 = after_running(res[6], res[0])  
                else:
                    result1 = after_running_on_macos(res[6], res[0])
                    
                if result == '':
                    result = result1
                update_flag = update_session_after_running(pc_name, res, start, Start_time, src_iso_path, result)   
                if not update_flag:
                    update_session_table(res, 2, res[0], res[1], pc_name, result = result)
                    initlog('the session table does not update before running\n')   
                                                        
                log_filename_list = get_log_files(logpath)      
                upload_file(log_filename_list, res[0])    
                if '.ISO' == os.path.splitext(res[6].upper())[1]: 
                    dest_path = os.path.split(res[6])[0]
                else:
                    dest_path = res[6]    
                    
                start_time = Start_time.replace('-','_') 
                start_time = start_time.replace(':','_')
                start_time = start_time.replace(' ','_') 
                copy_file(log_filename_list, dest_path)       
                try:
                    if os.name == 'nt':
                        zip_files(log_filename_list, dest_path + '\\' + start_time +'.zip')  
                    else:
                        zip_files(log_filename_list, dest_path + '/' + start_time +'.zip') 
                except Exception, e:
                    initlog('failed to zip file; ' + str(e))       
            if result != '':
                update_session_flag(3, res[0], res[1], pc_name)     
        else:
            result = 'not find Fab, maybe Fab path is error\n\n'
            update_session_table(res, 3, res[0], res[1], pc_name, result = result)
            initlog(result)  
        #if result != '':
        #        update_session_flag(3, res[0], res[1], pc_name)  


if __name__ == '__main__':
    main()
    print 'ok, this is end! This window will be closed after 10 seconds!!'    
    
    
 
 
 
