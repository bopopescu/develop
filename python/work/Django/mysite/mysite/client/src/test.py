#-*- encoding:utf-8 -*-
import subprocess
import MySQLdb
import _winreg
import time, datetime
import os
import socket
import logging

import ImageGrab
import zipfile
import ConfigParser
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump, Comment, tostring
#import win32api
#import win32con
#import win32gui
LOG_FILENAME = 'd:/test.log'


def connect_database():
    
    conn = ''
    cursor = ''
    
    try:
        conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '19890612')   
        conn.select_db('mysite')   
    except Exception, e:
        initlog(str(e))     
    else:
        cursor = conn.cursor()     
    return conn, cursor


def get_pcname():
    
    pc_name = ''
    
    try:   
        pc_name = socket.gethostname()       
    except Exception, e:
        initlog(str(e))            
    return pc_name


def get_ip(pc_name): 
    
    pc_ip = ''
     
    try:   
        pc_ip = socket.gethostbyname(pc_name)   
    except Exception, e:
        initlog(str(e))          
    return pc_ip

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
        initlog(str(e))     
    finally:
        cursor.close()     
        conn.close()     
    return  res


def res_to_iso(res):
    
    if '/' in res[4]:
        module = res[4].split('/')[-2].upper()                                                #BD, DVD, BD3D, FILE
        iso = res[4].split('/')[-1]                                                           #HUGO.iso 
    else:
        module = res[4].split('\\')[-2].upper()                                                #BD, DVD, BD3D, FILE
        iso = res[4].split('\\')[-1]                                                           #HUGO.iso
        
    return module, iso

 
def search_iso_path(module, iso):
    
    src_iso_path = '' 
    path_list = [r'\\10.10.2.58\nas_nas_volume1', r'\\10.10.2.58\nas_nas_volume2', r'\\10.10.2.59\nas_nas_volume5', r'\\10.10.2.56\Volume3', r'\\10.10.2.56\Volume4']                    
                    
    if 'DVD' == module:        
        for root, _, all_files in os.walk(r'\\10.10.2.58\nas_nas_volume2\DVD'):                
            for onefile in all_files:                
                if iso.upper()  == onefile.upper():                    
                    src_iso_path = os.path.join(root, onefile)
                    print 'DVD, src_iso_path:',src_iso_path    
                    return src_iso_path               
         
    elif 'VIDEO' == module:    
        for root, _, all_files in os.walk(r'\\10.10.2.58\nas_nas_volume2\File'):                
            for onefile in all_files:                
                if iso.upper()  == onefile.upper():
                    src_iso_path = os.path.join(root, onefile)
                    print 'file, src_iso_path:',src_iso_path   
                    return src_iso_path 
                
    else:                                                                                           #bd or 3d
        for path in path_list:      
            for root, _, all_files in os.walk(path): 
                for onefile in all_files:   
                    if iso.upper()  == onefile.upper():               
                        src_iso_path = os.path.join(root, onefile)                                                    
                        print 'BD or 3D, src_iso_path:',src_iso_path 
                        return src_iso_path               
         
            
def update_session_table(res, Flag, case_num, src_iso_path = '', Start_time = '', End_time = '', Total_time = '', Folder_size = '', result = ''):
    
    if src_iso_path == '':
        src_iso_path = res[4]
    if Start_time == '':
        Start_time = res[32]
        
    conn, cursor = connect_database()     
    sql = "update blog_session set Current_src_path = '%s', Flag = '%d', Start_time = '%s', End_time = '%s', Total_time = '%s', Folder_size = '%s', Result = '%s' where Num = '%s'" \
          % (src_iso_path, Flag, Start_time, End_time, Total_time, Folder_size, result, case_num) 
    try:      
        cursor.execute(sql)  
        conn.commit()  
    except Exception, e:        
        initlog(str(e))   
    finally:               
        cursor.close()    
        conn.close() 

    
def get_registry_value(regpath, regkey):
    
    value_path = ''
    
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, regpath, 0, _winreg.KEY_READ)
    try: 
        (value_path, valuetype) = _winreg.QueryValueEx(key, regkey)
    except Exception, e:
        initlog(str(e))  

    return value_path
    
    
def get_cmd_string(res, src_iso_path, client_dest_path):
    
    dest_path = res[5]
    Dest = '  /DEST '  + '"' + res[5] + '"'    
    Mode =  '  /MODE ' + '"' + res[3] + '"'    
    Src = '   /SRC ' + '"' + src_iso_path + '"'     
    Audio =  '  /AUDIO ' + '"' + res[8] + '"'    
    Audioid = '  /AUDIOID '
    
    Audio_type = '  /AUDIOTYPE ' + '"' + res[9] + '"'    
    Change_play_order = '  /CHANGEPLAYORDER ' + '"' + res[10] + '"'    
    Copy_IFO = '  /COPYIFO ' + '"' + res[11] + '"'    
    Display_forced_sub  =  '  /DISPLAYFORCEDSUB ' + '"' + res[12] + '"'    
    Jump_menu = '  /JUMPMENU ' + '"' + res[13] + '"'  
      
    Jump_main = '  /JUMOMAIN ' + '"' + res[14] + '"'    
    Out_disc = '  /OUTDISC ' + '"' + res[15] + '"'    
    Path_player = '  /PATHPLAYER ' + '"' + res[16] + '"'    
    Preserve_menu_disc2 = '  /PRESERVEMENUDISC2 ' + '"' + res[17] + '"'    
    Profile = '  /PROFILE ' + '"' + res[18] + '"'
    
    Remove_DTS = '  /REMOVEDTS ' + '"' + res[19] + '"'    
    Remove_HD_audio = '  /REMOVEHDAUDIO ' + '"' + res[20] + '"'    
    Remove_menu = '  /REMOVEMENU ' + '"' + res[21] + '"'    
    Remove_PGC = '  /REMOVEPGC ' + '"' + res[22] + '"'    
    Rewind = '  /REWIND ' + '"' + res[23] + '"'
    
    Subtitleid = '  /SUBTITLEID '
    Subtitle = '  /SUBTITLE ' + '"' + res[24] + '"'    
    Title = '  /TITLE ' + '"' + res[25] + '"'    
    Volume = '  /VOLUME ' + '"' + res[26] + '"'    
    Close = '  /CLOSE'    
    Createminiso = '  /CREATEMINISO'
    
    cmd_string = Mode + Src + Dest + Audio + Audioid + Audio_type + Change_play_order + Copy_IFO + Display_forced_sub + Jump_menu + Jump_main + Out_disc + Path_player \
                 + Preserve_menu_disc2 + Profile + Remove_DTS + Remove_HD_audio + Remove_menu + Remove_PGC + Rewind + Subtitleid + Subtitle + Title + Volume + Close + Createminiso
    
    return cmd_string, dest_path


def get_Filesize(dest_path): 
    
    Folder_size = 0  
    
    if os.path.exists(dest_path):   
        for root, _, all_files in os.walk(dest_path):                    
            for filespath in all_files:                     
                path_file = os.path.join(root, filespath)                           
                file_size = os.path.getsize(path_file)                        
                Folder_size += file_size                
        Folder_size = Folder_size/1024/1024
        
    else:
        initlog('the Folder path does not exist')
            
    return Folder_size  

def judge_filesize(res, Folder_size):
    
    result = ''
    
    if res[15].split(' ')[0] == 'bd50':
        if Folder_size < 18000 or Folder_size > 46100:
            result = 'the bd50 folder_size is error'
            initlog(result)
         
    elif res[15].split(' ')[0] == 'bd25':
        if Folder_size < 15000 or Folder_size > 23700:
            result = 'the bd25 folder_size is error'
            initlog(result)
            
    elif res[15].split(' ')[0] == 'bd9':
        if Folder_size < 4000 or Folder_size > 8100:
            result = 'the bd9 folder_size is error'  
            initlog(result) 
         
    elif res[15].split(' ')[0] == 'bd5':
        if Folder_size < 2000 or Folder_size > 4400:
            result = 'the bd5 folder_size is error'  
            initlog(result)
    else:
        pass
                   
    return result
           

def update_registry(path, valuename, value):

    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, path,  0, _winreg.KEY_ALL_ACCESS)    
    try:
        _winreg.SetValueEx(key, valuename, 0, _winreg.REG_DWORD, value)      
    except Exception, e:    
        initlog(str(e))
  
  
def initlog(info): 
    
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s - %(levelname)s: %(message)s')       
    logging.info(info) 

    
def check_process_exist(process_name):
    
    returncode = ''   
    try:
        p=os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name)   
        returncode = p.read().count(process_name)        
    except Exception, e:
        initlog(str(e))
        
    return returncode

def kill_process(process_name):
 
    try: 
        os.system('taskkill /f /im ' + process_name)        
    except Exception, e:
        initlog(str(e))         
    else:      
        print 'the process is killed'
        
        
def catch_all_picture(dest_path):
     
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S')   
    try:       
        pic = ImageGrab.grab()
        pic.save(dest_path+'/' + current_time + '.png')
    except Exception, e:
        initlog(str(e))
    

def read_ini(ini_file):
    
    bd_analysis_time = ''
    bd_interval_time = ''     
    dvd_analysis_time = ''  
    dvd_interval_time = ''
    
    if not os.path.exists(ini_file):  
        try:    
            file(ini_file, 'a')
        except Exception, e:
            initlog(str(e))
    
    config = ConfigParser.ConfigParser()
    
    try:
        config.readfp(open(ini_file))
    except Exception, e:
        initlog(str(e))      
    else:     
        bd_analysis_time = int(config.get('BD/3Dcopy','analysis time')) 
        bd_interval_time = int(config.get('BD/3Dcopy','interval time'))        
        dvd_analysis_time = int(config.get('DVD/FILEcopy','analysis time'))        
        dvd_interval_time = int(config.get('DVD/FILEcopy','interval time'))
    
    return bd_analysis_time, bd_interval_time, dvd_analysis_time, dvd_interval_time
    
    
def write_xml():
    
    '''
      <?xml version="1.0"?>
      <PurchaseOrder>
        <account refnum="2390094"/>
        <item sku="33-993933" qty="4">
          <name>Potato Smasher</name>
          <description>Smash Potatoes like never before.</description>
        </item>
      </PurchaseOrder>
    ''' 
    
    book = ElementTree()    
    purchaseorder = Element('PurchaseOrder')    
    book._setroot(purchaseorder)      
    SubElement(purchaseorder,  'account', {'refnum' : "2390094"})    
    item = Element("item", {'sku' : '33-993933', 'qty' : '4'})    
    purchaseorder.append(item)   
    SubElement(item, 'name').text = "Potato Smasher"    
    SubElement(item, 'description').text = "Smash Potatoes like never before."
        
    return book, purchaseorder


def indent(elem, level = 0):
    
    i = "\n" + level * "  "
    if len(elem):        
        if not elem.text or not elem.text.strip():            
            elem.text = i + "  "            
        for e in elem:            
            indent(e, level+1)            
        if not e.tail or not e.tail.strip():            
            e.tail = i
                        
    if level and (not elem.tail or not elem.tail.strip()):        
        elem.tail = i
               
    return elem


def read_xml():    
    
    purchaseorder = Element('interface')    
    SubElement(purchaseorder,  'model', {'type' : "vir"})    
    tree = ElementTree()    
    tree.parse('d:/wenjian/file.xml')    
    print purchaseorder.find('model').get('type')    
    print tree.find('alias').get('name')


def update_registry_value(res):
    
    if not res[27]:
        Video_decoder_H264 = 0      
    else:
        Video_decoder_H264 = int(res[27])
        
    if not res[28]:
        Video_decoder_VC1 = 0
    else:   
        Video_decoder_VC1 = int(res[28])
    
    if not res[29]:
        Video_decoder_MPEG2  = 0      
    else: 
        Video_decoder_MPEG2 = int(res[29])
        
    if not res[30]:
        Video_encoder_H264 = 0
    else:
        Video_encoder_H264 = int(res[30])
        
    if Video_decoder_H264 == 1 or Video_decoder_VC1 == 1 or Video_decoder_MPEG2 == 1:        
        enableGPUA = 1        
    else:      
        enableGPUA = 0
        
    update_registry_list = [('Software\\DVDFab\\V8_QT\\FileMover\\', 'EnableFileMover', 0), ('Software\\DVDFab\\V8_QT\\BluRayToBluRay\\', 'BDAVCHDCompatibility', 1), \
                            ('Software\\DVDFab\\V8_QT\\Generic\\', 'H264DecodeTypeUser_qt', 1), ('Software\\DVDFab\\V8_QT\\Generic\\', 'VC1DecodeTypeUser_qt', 1),\
                            ('Software\\DVDFab\\V8_QT\\Generic\\', 'Mpeg2DecodeTypeUser_qt', 1), ('Software\\DVDFab\\V8_QT\\Generic\\', 'EnableCudaEncodingUser_qt', 1),\
                            ('Software\\DVDFab\\V8_QT\\Generic\\', 'EnableDirectTranscoderUser_qt', 1), ("Software\\DVDFab\\V8_QT\\Generic\\", 'H264DecodeType_qt', Video_decoder_H264),\
                            ("Software\\DVDFab\\V8_QT\\Generic\\", 'VC1DecodeType_qt', Video_decoder_VC1), ("Software\\DVDFab\\V8_QT\\Generic\\", 'Mpeg2DecodeType_qt', Video_decoder_MPEG2),\
                            ("Software\\DVDFab\\V8_QT\\Generic\\", 'EnableCudaEncoding_qt', Video_encoder_H264), ("Software\\DVDFab\\V8_QT\\Generic\\", 'EnableGPUAccelerate_qt', enableGPUA)]
    
    try:
        for record in update_registry_list:           
            update_registry(record[0],record[1],record[2])            
    except Exception, e:            
            initlog(str(e))

    
def remove_fab_logfile(fab_logpath):

    if os.path.exists(fab_logpath):
        files = os.listdir(fab_logpath)    
        for onefile in files:        
            path_file = os.path.join(fab_logpath, onefile)        
            try:
                os.remove(path_file)            
            except Exception, e:            
                initlog(str(e))
    else:
        initlog('the fab_logpath does not exist')  
               
            
def get_log_files(logpath):
    
    log_filename_list = []
    
    if logpath:
        for path in logpath:    
            for root, _, files in os.walk(path):                
                for onefile in files:                
                    path_file = os.path.join(root, onefile)                
                    log_filename_list.append(path_file)
    else:
        initlog('the logpath does not exist')    
    return log_filename_list

 
def zip_files(log_filename_list, zipfilename):
    
    if log_filename_list:
        zf = zipfile.ZipFile(zipfilename, 'w', zipfile.zlib.DEFLATED)    
        for log_filename in log_filename_list:        
            try:
                zf.write(log_filename)        
            except Exception, e:            
                initlog(str(e)) 
                
        zf.close()
        
    else:
        initlog('the files who are needed to zip does not exist')
                       

def start_running(DVDFab_path_cmd_string, module, dest_path, bd_analysis_time, bd_interval_time, dvd_analysis_time, dvd_interval_time, burn_engine_type):
    
    result = ''
    
    try:       
        p = subprocess.Popen(DVDFab_path_cmd_string)       
    except Exception, e:        
        initlog(str(e))        
        catch_all_picture(dest_path)        
        result = 'Exception, Autotest tool raise error; '
        initlog(result)
    else: 
        if module == 'BD':                               
            for i in range(bd_analysis_time):                
                if not p.poll():                    
                    time.sleep(60)                 
                else:                    
                    catch_all_picture(dest_path)                    
                    result = 'Autotest tool raise error in bd_analysis_time; '    
                    initlog(result)                
                    return  result                                                                         
            flag = 1            
            number = 0                        
            while flag:      
                First_size = get_Filesize(dest_path)                
                initlog('First_size: ' + str(First_size))
                flag = 0        
                number += bd_interval_time * 30                                                          
                if not p.poll():                    
                    flag = 1            
                    time.sleep(bd_interval_time * 30)                    
                    if number == bd_interval_time * 60:                        
                        number = 0 
                        Last_size = get_Filesize(dest_path) 
                        initlog('Last_size: ' + str(Last_size))
                        if Last_size - First_size <= 0:                                                    
                            flag = 0                                  
                            print 'exception in bd_interval_time'                                                     
                            catch_all_picture(dest_path)                            
                            result = 'Autotest tool raise error in bd_interval_time; '     
                            initlog(result)                   
                        else:                        
                            print 'ok, success'  
                                                                             
        else:              
            for i in range(dvd_analysis_time):               
                if not p.poll():                    
                    time.sleep(60)                       
                else:                    
                    catch_all_picture(dest_path)                    
                    result = 'Autotest tool raise error in dvd_analysis_time; ' 
                    initlog(result)                   
                    print result                    
                    return  result                                                                    
            flag = 1            
            number = 0                        
            while flag:               
                First_size = get_Filesize(dest_path)            
                initlog('First_size: ' + str(First_size))            
                flag = 0                
                number += dvd_interval_time * 30                      
                if not p.poll():                    
                    flag = 1            
                    time.sleep(dvd_interval_time * 30)                    
                    if number == dvd_interval_time * 60:                        
                        number = 0 
                        Last_size = get_Filesize(dest_path)   
                        initlog('Last_size: ' + str(Last_size))                    
                        if Last_size - First_size <= 0:                       
                            flag = 0       
                            print 'exception in dvd_interval_time'                                                                                             
                            catch_all_picture(dest_path)                            
                            result = 'Autotest tool raise error in dvd_interval_time; '
                            initlog(result)
                        else:                        
                            print 'ok, success'    
                                                                          
        return result
    

def tempfolder(burn_engine_type):
    
    if burn_engine_type == 0:
        time.sleep(3600)


def before_running(res, src_iso_path, client_dest_path, DVDFab_path):

    cmd_string, dest_path = get_cmd_string(res, src_iso_path, client_dest_path) 
    DVDFab_path_cmd_string = DVDFab_path + cmd_string  
    initlog(DVDFab_path_cmd_string)
    
    fab_logpath = get_registry_value("Software\\DVDFab\\V8_QT\\Generic", "LogFolder")           
    burn_engine_type = get_registry_value("Software\\DVDFab\\V8_QT\\DVD\\", 'BurnEngineType')
    tempfolder_path = get_registry_value("Software\\DVDFab\\V8_QT\\Generic\\", 'TempFolder') 
     
    if '.ISO' == os.path.splitext(res[5].upper())[1]:           
        dest_path = tempfolder_path       
        
    tempfolder_path = ''.join((tempfolder_path, 'ReportCrash'))     
    logpath = (fab_logpath, tempfolder_path)         
    remove_fab_logfile(fab_logpath)
    initlog('before running: ' + dest_path)
    return DVDFab_path_cmd_string, dest_path, logpath, burn_engine_type


def update_session_before_running(src_iso_path, res):
    
    start = datetime.datetime.now()      
    Start_time = str(start).split('.')[0]          
    src_iso_path = src_iso_path.replace('\\','\\\\')    
    update_session_table(res, 1, res[1], src_iso_path, Start_time) 
    return start, Start_time, src_iso_path 
 

def update_session_after_running(res, start, Start_time, src_iso_path, result):
    
    dest_path = res[5]
    if '.ISO' == os.path.splitext(dest_path.upper())[1]: 
        dest_path = os.path.split(dest_path)[0]
    end = datetime.datetime.now()    
    End_time = str(end).split('.')[0]    
    Total_time = (end - start).seconds    
    Total_time = str(Total_time/3600)+':'+str(Total_time%3600/60)+':'+str(Total_time%3600%60%60)           
    Folder_size = get_Filesize(dest_path)  
    result1 = judge_filesize(res, Folder_size) 
    result += result1
    initlog('after running, after Folder_size: ' + dest_path)
    update_session_table(res, 2, res[1], src_iso_path, Start_time, End_time, Total_time, Folder_size, result)
    
    
def after_running(dest_path):
    
    result = ''
    process_list = ["DVDFab.exe", "WerFault.exe", "dwwin.exe", "FabReport.exe"]
    
    if '.ISO' == os.path.splitext(dest_path.upper())[1]: 
        dest_path = os.path.split(dest_path)[0]
    
    for process_name in process_list:
        returncode = check_process_exist(process_name)     
        if returncode:    
            catch_all_picture(dest_path)        
            kill_process(process_name)
            result += process_name + ' is killed and the picture is catched by computer; '
            initlog(result)
    return result


def running(res, client_dest_path, DVDFab_path):
     
    start = ''
    Start_time = ''
    dest_path = ''
    result = ''
    logpath = ''
    burn_engine_type = ''
    
    update_registry_value(res)         
    module, iso = res_to_iso(res)       
    src_iso_path = search_iso_path(module, iso)  
          
    if src_iso_path:  
        DVDFab_path_cmd_string, dest_path, logpath, burn_engine_type = before_running(res, src_iso_path, client_dest_path, DVDFab_path)
        start, Start_time, src_iso_path = update_session_before_running(src_iso_path, res)  
        bd_analysis_time, bd_interval_time, dvd_analysis_time, dvd_interval_time = read_ini('d:/read.ini')         
        result = start_running(DVDFab_path_cmd_string, module, dest_path, bd_analysis_time, bd_interval_time, dvd_analysis_time, dvd_interval_time, burn_engine_type)      
    else:
        result = 'does not find case, the iso does not exist'
        initlog(result)
        print result  
        
    return start, Start_time, dest_path, src_iso_path, result, logpath, burn_engine_type

    
def main():
    
    dest_path = 'd:'
    pc_name = get_pcname()       
    client_ip, client_dest_path = get_ip_address(pc_name)  
    
    while 1:     
        res = search_session_table(pc_name)
        if not res:        
            print 'sorry , does not have any case for you'   
            initlog('sorry , does not have any case for you')        
            return 
        
        DVDFab_path = get_registry_value("Software\\DVDFab\\V8_QT", 'path')   
        
        if DVDFab_path:         
            start, Start_time, dest_path, src_iso_path, result, logpath, burn_engine_type = running(res, client_dest_path, DVDFab_path)
            if '.ISO' == os.path.splitext(res[5].upper())[1]: 
                tempfolder(burn_engine_type) 
                
            if start == '':
                update_session_table(res, 2, res[1])
                initlog('the session table does not update before running')
            else:             
                result1 = after_running(res[5])  
                result += result1
                update_session_after_running(res, start, Start_time, src_iso_path, result)            
                log_filename_list = get_log_files(logpath)        
                zip_files(log_filename_list, dest_path + '.zip')
        else:
            update_session_table(res, 2, res[1])
            initlog('does not find DVDFab.exe')       
                  

if __name__ == "__main__":
    
    main()
    print 'ok, end'
 
 
 
 
 
    
    
    
    