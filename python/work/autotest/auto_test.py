#-*- encoding:utf-8 -*-
"""
   @author: dedong.xu
   @description: 自动化case脚本，添加一些case之后，该工具先检测用户本地是否安装了DVDFab，如果安装就和数据库进行交互，检索到指定的用户名的case之后，
                 按队列形式一个一个的跑case，期间会计算生成的目录大小，定时检测目录是不是在变化。最后对目录大小进行判定，是否正常；
				 如果期间有什么错误发生，程序会自动截屏，并将log打包上传到服务器端。
				 操作注册表，读取ini配置文件，操作xml文件。
				 
"""
#standard lib
import subprocess
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

#3rd lib
import MySQLdb

user_name = getpass.getuser()
xml_temp = 'C:\\Users\\' + user_name + '\\AppData\\Roaming\\DVDFab9\\temp.xml'

current_path = os.getcwd()
TESTBAT_PATH = current_path +'/test.bat'
INI_FILE = current_path + '/dvdfab_auto_tool.ini'

if os.name == 'nt':
    import windows_xml
    KILL_DVDFAB_PATH = current_path +'/kill_DVDFab.bat'
else:
    import myxml
    DVDFAB_PATH = '/Applications/"DVDFab 9.app"/Contents/MacOS/DVDFab'  


def get_documents_path():
    """ get personal documents path """
    system_name = platform.platform().upper()
    if "XP" in system_name:
        documents_path = os.path.join(os.path.expanduser("~"), "My Documents")
    else:
        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    return documents_path

documents_path = get_documents_path()
LOG_FILENAME = documents_path + '/test.log'


def connect_database():    
    """ connect db """
    conn = ''
    cursor = ''
    try:
        conn = MySQLdb.connect(host = '10.10.3.25', user = 'root', passwd = '19890612')   
        conn.select_db('mysite')    
    except Exception, e:
        initlog('failed to connect database; %s' % str(e))  	
    else:
        cursor = conn.cursor()     
    return conn, cursor


def get_pcname():   
    """ get pc name by socket module """ 
    pc_name = ''  
    try:   
        pc_name = socket.gethostname()       
    except Exception, e:
        initlog('failed to get PC name; %s' % str(e))            
    return pc_name


def get_ip(pc_name):     
    """ get ip by pc name use socket """
    pc_ip = ''    
    try:   
        pc_ip = socket.gethostbyname(pc_name)   
    except Exception, e:
        initlog('failed to get PC ip; %s' % str(e))          
    return pc_ip


def get_client_path(pc_ip):
    """ get client path from db"""
    pc_name = ''
    client_dest_path = ''
    conn, cursor = connect_database() 
    sql = "select PC_name, Dest_path from blog_client where PC_ip = '%s'" % pc_ip
    try:
        cursor.execute(sql)
        pc_name, client_dest_path = cursor.fetchone()   
        conn.commit() 
    except Exception, e:      
        initlog("get client path failed: %s" % str(e))   
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
  
    
def get_all_cases(pc_name):    
    """ get all cases """
    res = '' 
    conn, cursor = connect_database()
    sql = " select * from blog_session where  PC_name = '%s' and (Flag = 0 or Flag =  1) " % pc_name  
    try:
        cursor.execute(sql)
        res = cursor.fetchall()    
        conn.commit() 
    except Exception, e: 
        initlog('failed to search session table; %s' % str(e))     
    finally:
        cursor.close()     
        conn.close()     
    return  res


def res_to_iso(res):
    #module:  BD, DVD, BD3D, FILE;   iso: HUGO.iso 
    module, iso = res[5].replace("\\", "/").split('/')[-2].upper(), res[5].replace("\\", "/").split('/')[-1]
    ripper_mode = res[4]
    return module, iso, ripper_mode
	
	
def get_path_list(path, path_mac):
    return (path.split(','), path_mac.split(',')) if ',' in path else (path.split(';'), path_mac.split(';'))
	
	
def get_iso_path(src_iso_path, iso, dvd_path_list):
    """ get iso from the given path, if found then break the loop """
    for path in dvd_path_list:               
        for root, _, all_files in os.walk(path.strip()):
            for onefile in all_files:                
                if iso.upper()  == onefile.upper():                    
                    src_iso_path = os.path.join(root, onefile)  
                    initlog("find iso: %s" % src_iso_path)
                    break
    return src_iso_path 
	
	
def connect_server(path, ip):
    """ use smb to connect server """
    if not os.path.exists(path):
        os.system('open smb://%s'%ip)
        time.sleep(20)
		
		
def get_final_iso_path(dvd_path_list, file_path_list, bd_path_list, module, iso):
    src_iso_path = ""
    cate_dict = {"DVD":dvd_path_list, "VIDEO":file_path_list}#, "BD":bd_path_list}
    if module in cate_dict:
        path_list = cate_dict[module]
    else:
        path_list = bd_path_list
    src_iso_path = get_iso_path(src_iso_path, iso, path_list)
    return src_iso_path
		
 
def search_iso_path(module, iso, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac): 
    """ search iso path """   
    src_iso_path = '' 
    try:
        bd_path_list, bd_path_mac_list = get_path_list(bd_path, bd_path_mac)
        dvd_path_list, dvd_path_mac_list = get_path_list(dvd_path, dvd_path_mac)
        file_path_list, file_path_mac_list = get_path_list(file_path, file_path_mac)
    except Exception, e:
        initlog('ini file is error; %s' % str(e))
    
    #windows
    if os.name == 'nt':     
        src_iso_path = get_final_iso_path(dvd_path_list, file_path_list, bd_path_list, module, iso)  
    #mac os          
    else:
        try:
            connect_server('/Volumes/nas2_nas2_volume3', '10.10.2.56')
            connect_server('/Volumes/nas3_nas3_Volume5', '10.10.2.59')
            src_iso_path = get_final_iso_path(dvd_path_mac_list, file_path_mac_list, bd_path_mac_list, module, iso)			
        except Exception, e:
            initlog('does not execute the command to connect server; %s' % str(e))         
             		
    return src_iso_path
                     
     
def update_session_table(res, Flag, case_id, case_num, pc_name, src_iso_path = '', Start_time = '', End_time = '', Total_time = '', Folder_size = '', result = ''):    
    update_flag = True
    src_iso_path = res[5] if src_iso_path == '' else src_iso_path
    Start_time = res[33] if Start_time == '' else Start_time
    conn, cursor = connect_database()     
    sql = "update blog_session set Current_src_path = '%s', Flag = '%d', Start_time = '%s', End_time = '%s', Total_time = '%s', Folder_size = '%s', Result = '%s' where id = '%d' and  Num = '%s' and PC_name = '%s' and (Flag = 0 or Flag =  1)" \
          % (src_iso_path, Flag, Start_time, End_time, Total_time, Folder_size, result, case_id, case_num, pc_name) 
    initlog("sql cmd is : %s" % sql)
    try:      
        cursor.execute(sql)  
        conn.commit()   
        initlog("update_session_table, the session table update")
    except Exception, e: 
        initlog('failed to update session table; %s' % str(e)) 
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
        initlog('failed to update session table; %s' % str(e)) 
    finally:               
        cursor.close()    
        conn.close() 
    
#this function does not be used    
def get_registry_value(regpath, regkey):  
    value_path = ''  
    if os.name == "nt":
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, regpath, 0, _winreg.KEY_READ)
        #key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, regpath, 0, _winreg.REG_SZ)
        try: 
            (value_path, valuetype) = _winreg.QueryValueEx(key, regkey)
        except Exception, e:
            initlog('failed to get registry value; %s' % str(e))   
    return value_path
		
		
def get_value(value, param):
    """ 格式化字符串输出 """
    return '  %s "%s"' % (param, value) if value else ""
    
    
def get_cmd_string(res, DVDFab_path, src_iso_path, client_dest_path): 
    """ get DVDFab cmd string """   
    dest_path = change_fuhao(res[6])
    Dest = get_value(res[6], "/DEST")
    Mode = get_value(res[4], "/MODE")
    Src = get_value(src_iso_path, "/SRC")
    Audio = get_value(res[9], "/AUDIO")
    Audio_type = get_value(res[10], "/AUDIOTYPE")
    Change_play_order = get_value(res[11], "/CHANGEPLAYORDER")
    Copy_IFO = get_value(res[12], "/COPYIFO")
    Display_forced_sub = get_value(res[13], "/DISPLAYFORCEDSUB")
    Jump_menu = get_value(res[14], "/JUMPMENU")
    Jump_main = get_value(res[15], "/JUMPMAIN")
    Out_disc = get_value(res[16], "/OUTDISC")
    Path_player = get_value(res[17], "/PATHPLAYER")
    Preserve_menu_disc2 = get_value(res[18], "/PRESERVEMENUDISC2")
    Profile = get_value(res[19], "/PROFILE")
    Remove_DTS = get_value(res[20], "/REMOVEDTS")
    Remove_HD_audio = get_value(res[21], "/REMOVEHDAUDIO")
    Remove_menu = get_value(res[22], "/REMOVEMENU")
    Remove_PGC = get_value(res[23], "/REMOVEPGC")
    Rewind = get_value(res[24], "/REWIND")
    Subtitle = get_value(res[25], "/SUBTITLE")
    Title = get_value(res[26], "/TITLE")
    Volume = get_value(res[27], "/VOLUME")
    BD3DT = get_value(res[44], "/BD3DCONVERTTYPE")
    COMPRESSTOAC3 = get_value(res[45], "/COMPRESSTOAC3")
    Close = '  /CLOSE'    
    Createminiso = '  /CREATEMINISO' if os.name == 'nt' else ''
    cmd_string = Mode + Src + Dest + Audio + Audio_type + Change_play_order + Copy_IFO + Display_forced_sub + Jump_menu + Jump_main\
                 + Out_disc + Path_player + Preserve_menu_disc2 + Profile + Remove_DTS + Remove_HD_audio + Remove_menu + Remove_PGC\
                 + Rewind + Subtitle + Title + Volume + BD3DT + COMPRESSTOAC3 + Close + Createminiso
    DVDFab_path_cmd_string = '"' + DVDFab_path + '"' + cmd_string  
    initlog('the cmd_string: %s' % DVDFab_path_cmd_string)
    return DVDFab_path_cmd_string, dest_path


def get_Filesize(dest_path): 
    """ get folder size """    
    Folder_size = 0  
    for root, _, all_files in os.walk(dest_path):                    
        for filespath in all_files:                                              
            file_size = os.path.getsize(os.path.join(root, filespath))                        
            Folder_size += file_size     

    return Folder_size
	
	
def judge_filesize1(foldersize, big_size, small_size, type_name):
    """ 判断文件大小 """
    if foldersize < small_size:
        result = 'folder_size too small; '
    elif foldersize > big_size:
        result = 'folder_size too big; '
    else:
        result = 'the %s folder_size is normal; ' % type_name
    return result


def judge_filesize(res, Folder_size):  
    """ 判断文件大小 """  
    Folder_size = int(Folder_size.split('.')[0])
    result = ''
    if res[3].upper() == 'BD' and res[4].upper() == 'FULLDISC':
        for record in [("bd50", 46100, 18000), ("bd25", 23000, 15000),("bd9", 8100, 4000),("bd5", 4300, 2000)]:
            if res[16].upper().startswith(record[0].upper()):
                if res[16].upper().startswith('BD5') and not res[16].upper().startswith('BD50'):
                    result = judge_filesize1(Folder_size, record[1], record[2], record[0])
        
    elif res[3].upper() == 'DVD' and res[4].upper() == 'FULLDISC' or res[3].upper() == 'BD' and res[4].upper() == 'BLURAYDVD':
        for record in [("dvd5", 4300, 2000), ("dvd9", 8100, 4000)]:
            if res[16].upper().startswith(record[0].upper()):
                result = judge_filesize1(Folder_size, record[1], record[2], record[0])
			
	initlog(result)        
    return result
           

def update_registry(path, valuename, value):
    import _winreg
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, path,  0, _winreg.KEY_ALL_ACCESS)    
    try:
        _winreg.SetValueEx(key, valuename, 0, _winreg.REG_DWORD, value)      
    except Exception, e:
        initlog('failed to update registry; %s' % str(e))
  
  
def initlog(info):     
    #logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s - %(levelname)s: %(message)s') 
    logging.basicConfig(filename = LOG_FILENAME, level = logging.NOTSET, filemode = 'a', format = '%(asctime)s : %(message)s')      
    logging.info(info) 
    
    
def check_process_exist(process_name):  
    """ check process, only used in windows """  
    returncode = ''   
    try:
        p=os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name) 
        returncode = p.read().count(process_name) 
        if returncode:
            initlog('%s exists' % process_name)
    except Exception, e:
        initlog(str(e))   
    return returncode


def kill_process(process_name): 
    """ kill process """
    try: 
        os.system('taskkill /f /im %s' % process_name)      
        initlog('%s is killed now' % process_name)		
    except Exception, e:
        initlog('failed to kill process; %s' % str(e))      

        
def catch_all_picture(picture_path, index):   
    """ 截取屏幕 """  
    initlog('picure_path: %s' % picture_path)
    current_time = time.strftime('%Y-%m-%d-%H-%M-%S')   
    if os.name == 'nt':
        try:       
            import ImageGrab
            pic = ImageGrab.grab()
            pic.save(os.path.join(picture_path, "%d-%s.png" % (index, current_time)))
            initlog('success to catch the picture')
        except Exception, e:
            initlog('failed to catch the picture; %s' % str(e))
    else:
        try:
            os.system('screencapture ' +  picture_path + '/' + str(index) + '-' + current_time + '.png')
            initlog('success to catch the picture')
        except Exception, e:
            initlog('failed to catch the picture; %s' % str(e))
            

def read_ini(ini_file):    
    project = ''
    bd_analysis_time = bd_interval_time = '' 
    bd_ripper_analysis_time = bd_ripper_interval_time = ''    
    dvd_analysis_time = dvd_interval_time = ''  
    file_analysis_time = file_interval_time = ''  
    bd_path = dvd_path = file_path = ''
    bd_path_mac = dvd_path_mac = file_path_mac = ''
    params_dict = {}
    
    if os.path.exists(ini_file):           
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(ini_file))
        except Exception, e:
            initlog('failed to read ini file; %s' % str(e))      
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
                initlog('read ini file error; %s' % str(e))
    else:
        initlog('dvdfab_auto_tool.ini file does not exist')
    params_dict["project"] = project
    params_dict["bd_analysis_time"] = bd_analysis_time
    params_dict["bd_interval_time"] = bd_interval_time
    params_dict["bd_ripper_analysis_time"] = bd_ripper_analysis_time
    params_dict["bd_ripper_interval_time"] = bd_ripper_interval_time
    params_dict["dvd_analysis_time"] = dvd_analysis_time
    params_dict["dvd_interval_time"] = dvd_interval_time
    params_dict["file_analysis_time"] = file_analysis_time
    params_dict["file_interval_time"] = file_interval_time
    params_dict["bd_path"] = bd_path
    params_dict["dvd_path"] = dvd_path
    params_dict["file_path"] = file_path
    params_dict["bd_path_mac"] = bd_path_mac
    params_dict["dvd_path_mac"] = dvd_path_mac
    params_dict["file_path_mac"] = file_path_mac
    return params_dict
    return project, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time, dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, bd_path, dvd_path, file_path,bd_path_mac,dvd_path_mac,file_path_mac


def convert_to_int(value):
    """ 转换成整型 """
    return int(value) if value else 0
    

def update_registry_value(res, project, XML_FILE):   
    """ 更新注册表的值 """
    Video_decoder_H264 = convert_to_int(res[28]) 
    Video_decoder_VC1 = convert_to_int(res[29])
    Video_decoder_MPEG2 = convert_to_int(res[30])
    Video_encoder_H264 = convert_to_int(res[31])
    enableGPUA = 1 if Video_decoder_H264 == 1 or Video_decoder_VC1 == 1 or Video_decoder_MPEG2 == 1 else 0
    path_list = ["common_setting/FileMover","common_setting/BluRayToBluRay","common_setting/Generic","common_setting/DVD"]
    if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':  
        update_key_value_list = [('ShowWelcome', '0'),('EnableFileMover', '0'),('BDAVCHDCompatibility', '1'),('H264DecodeTypeUser_qt', '1'),('VC1DecodeTypeUser_qt', '1'),('Mpeg2DecodeTypeUser_qt', '1'),\
								('EnableCudaEncodingUser_qt', '1'),('EnableDirectTranscoderUser_qt', '1'),('H264DecodeType_qt', str(Video_decoder_H264)),('VC1DecodeType_qt', str(Video_decoder_VC1)),\
								('Mpeg2DecodeType_qt', str(Video_decoder_MPEG2)),('EnableCudaEncoding_qt', str(Video_encoder_H264)),('EnableGPUAccelerate_qt', str(enableGPUA)),('NotShowSetBDRegion', '1'),\
								('AskOveride', '0')] 
    else:
        update_key_value_list = [('ShowWelcome', '0'),('EnableFileMover', '0'),('BDAVCHDCompatibility', '1'),('H264DecodeTypeUser_qt', '1'),('VC1DecodeTypeUser_qt', '1'),('Mpeg2DecodeTypeUser_qt', '1'),\
								('EnableCudaEncodingUser_qt', '1'),('EnableDirectTranscoderUser_qt', '1'),('H264DecodeType_qt', str(Video_decoder_H264)),('VC1DecodeType_qt', str(Video_decoder_VC1)),\
								('Mpeg2DecodeType_qt', str(Video_decoder_MPEG2)),('EnableCudaEncoding_qt', str(Video_encoder_H264)),('EnableDirectTranscoder_qt', str(enableGPUA)),('NotShowSetBDRegion', '1'),\
								('AskOveride', '0')] 

    if os.name == 'nt':
        for path in path_list:
            try:
                tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
            except Exception, e:
                initlog('%s does not exist; %s'(path, str(e)))
            else:
                for record in update_key_value_list:
                    if nodes[0].attrib.has_key(record[0]):
                        windows_xml.update_xml(nodes, record[0], record[1]) 
                windows_xml.write_xml(tree, XML_FILE)            
    else:
        for path in path_list:
            try:
                tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp)  
            except Exception, e:
                initlog('%s does not exist; %s'(path, str(e)))
            else:
                for record in update_key_value_list:
                    if nodes[0].attrib.has_key(record[0]):
                        myxml.update_xml(nodes, record[0], record[1]) 
                myxml.write_xml(tree, XML_FILE)
 
    
def remove_fab_logfile(fab_logpath):
    """ 在跑case之前，先清空之前的log文件 """
    if os.path.exists(fab_logpath):
        files = os.listdir(fab_logpath)    
        for onefile in files:                
            try:
                os.remove(os.path.join(fab_logpath, onefile))   				
            except Exception, e:
                initlog('fail to remove log files; %s' % str(e))
    else:
        initlog('cannot remove fab logfiles, log and temp do not exist')  
               
            
def get_log_files(logpath):    
    """ 获取所有的log文件 """
    log_filename_list = []
    if logpath:
        for path in logpath:  
            for root, _, files in os.walk(path):                
                for onefile in files: 
                    if os.path.splitext(onefile)[1].lower()  == '.bin' or os.path.join(root, onefile).find("BDMV") != -1:      
                        continue   
                    else:            
                        log_filename_list.append(os.path.join(root, onefile))
                        initlog("log_filename_list: %s" % str(log_filename_list))
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
    """ 压缩最后运行结果的log文件 """  
    initlog("zip files log_filename_list: %s" % str(log_filename_list))
    if log_filename_list:
        zf = zipfile.ZipFile(zipfilename, 'a', zipfile.zlib.DEFLATED)      
        for log_filename in log_filename_list:     
            try:
                if '/TEMP/' in log_filename.upper() or '\\TEMP\\' in log_filename.upper():
                    zf.write(log_filename, "temp" + os.sep  + os.path.split(log_filename)[1], zipfile.ZIP_DEFLATED)
                else:
                    zf.write(log_filename, "log" + os.sep + os.path.split(log_filename)[1], zipfile.ZIP_DEFLATED)        
            except Exception, e:
                initlog('failed to zip files; %s' % str(e))                
        zf.close()
        
    else:
        initlog('log and temp to be ziped does not exist!')
                       

def upload_file(log_filename_list, index):  
    """use ftp to upload file"""
    initlog("begin to upload files to server!!!!!!!")  
    for filename in log_filename_list:
        ftp_server = '10.10.3.25'
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
            initlog('failed to upload files; %s' % str(e))
        else:
            file_handler.close()
        finally:
            ftp.quit()


def get_picture_path(path):
    """ 获取图片的保存目录 """
    return change_fuhao(os.path.split(path)[0] if os.path.splitext(path.upper())[1] == '.ISO' else path)

def create_folder(folder):
    """ create folder if not exist """
    flag = True
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            initlog('Folder path:%s created by me; ' % folder) 
        except Exception, e:
            initlog('failed to create Folder path; %s' % str(e))
            flag = False
    return flag
	

def call_test_bat(test_bat):
    """ 调用Sikuli脚本来杀死DVDFab """
    try:
	    subprocess.call(test_bat)
	    initlog("DVDFab may killed by Sikuli")
    except Exception, e:
	    initlog("DVDFab does not killed by Sikuli") 
    	
def is_break_loop(p, analysis_time, dest_path1, re):
    """ 判断是否跳出循环 """
    result = ""
    flag = False
    for i in range(analysis_time):               
        if p.poll() is None:                    
            time.sleep(60)                      
        else:   
            catch_all_picture(dest_path1, re)                 
            flag = True	
            result = 'Fab killed in the beginning; '                 
            initlog(result)                
            break			
    return flag, result
	
def get_right_analysis_and_interval_time(module,ripper_mode,bd_analysis_time,bd_interval_time,bd_ripper_analysis_time,bd_ripper_interval_time,dvd_analysis_time,dvd_interval_time, file_analysis_time, file_interval_time):
    """ 根据case的类型，类获取分别对应的分析时间以及间隔时间 """
	if module == "BD": 
		if ripper_mode.upper() == "RIPPER":
			initlog("this case is ripper")
			bd_analysis_time = bd_ripper_analysis_time	
			bd_interval_time = bd_ripper_interval_time	
		analysis_time, interval_time = bd_analysis_time, bd_interval_time				                                                 
    elif module == 'DVD': 
		analysis_time, interval_time = dvd_analysis_time, dvd_interval_time			                        
    else: 
		analysis_time, interval_time = file_analysis_time, file_interval_time
    return analysis_time, interval_time
		
    
def start_running(res, DVDFab_path_cmd_string, module, ripper_mode, dest_path, bd_analysis_time, bd_interval_time, bd_ripper_analysis_time, bd_ripper_interval_time,dvd_analysis_time, dvd_interval_time, file_analysis_time, file_interval_time, burn_engine_type, client_dest_path):    
    """ run DVDFab cmd string """
    result = ""
    try:       
        p = subprocess.Popen(DVDFab_path_cmd_string, shell = True) 
        initlog("now, DVDFab starts running")
    except Exception, e:
        result = "DVDFab failed to run; "
        initlog("%s, %s"%(result, str(e))) 
    else: 
        dest_path1 = change_fuhao(os.path.split(res[6])[0] if ".ISO" == os.path.splitext(res[6].upper())[1] else res[6])
        folder_flag = create_folder(dest_path1)	 
        analysis_time, interval_time = get_right_analysis_and_interval_time(module,ripper_mode,bd_analysis_time,bd_interval_time,bd_ripper_analysis_time,bd_ripper_interval_time,dvd_analysis_time,dvd_interval_time, file_analysis_time, file_interval_time)			
        initlog("the analysis_time is beginning, please wait for %d mins" % analysis_time)
        loop_flag, result = is_break_loop(p, analysis_time, dest_path1, res[0])
        if loop_flag: 
			return result 
        initlog('the analysis_time is over')                                                                      
        flag = 1            
        number = 0                        
        while flag:
            if not folder_flag:
                break
            First_size = get_Filesize(dest_path)        
            initlog('First_size: %s' % str(First_size))
            flag = 0        
            number += interval_time                                                          
            if p.poll() is None:                   
                flag = 1            
                time.sleep(interval_time * 30)                    
                if number == interval_time * 2:                        
                    number = 0 
                    Last_size = get_Filesize(dest_path) 
                    initlog('Last_size: %s' % str(Last_size))
                    if Last_size <= First_size:
                        flag = 0    
                        time.sleep(120)
                        if p.poll() is None:
                            if '.ISO' == os.path.splitext(res[6].upper())[1]:
                                tempfolder_to_iso(burn_engine_type, res[6])
                            else:
                                initlog('*****DVDFab still exists')   
                                picture_path = get_picture_path(res[6])                                                                                              
                                catch_all_picture(picture_path, res[0])                         
                                result = 'Freeze and cancel dvdfab; ' if result == '' else result     
                                initlog(result)
                                call_test_bat(TESTBAT_PATH) 			
    return result
    

def tempfolder_to_iso(burn_engine_type, dest_path):   
    dest_path = change_fuhao(dest_path)
    initlog('tempfolder to iso is beginning!')
    dest_path = os.path.split(dest_path)[0]
    for i in range(6):    
        flag = create_folder(folder)
        if flag == False:
            break		
        First_size = get_Filesize(dest_path)
        initlog('First_size: %s' % str(First_size)) 
        time.sleep(600)
        Last_size = get_Filesize(dest_path)
        initlog('Last_size: %s' % str(Last_size))
        if Last_size <= First_size:
            break
    initlog('tempfolder to iso is over')


def get_xml_value(node, key):
    """ 根据给定的键值，获取xml文档里的value值 """
    return node.attrib[key] if node.attrib.has_key(key) else ""


def before_running(res, src_iso_path, dest_path, project, XML_FILE): 
    path_list = ["common_setting/Generic","common_setting/DVD"]
    if os.name == 'nt':
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':
            for path in path_list:
                tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
                fab_logpath = get_xml_value(nodes[0], 'LogFolder')
                burn_engine_type = get_xml_value(nodes[0], 'BurnEngineType')
                tempfolder_path = get_xml_value(nodes[0], 'TempFolder')
        else:
            for path in path_list:
                tree, nodes = windows_xml.read_xml(XML_FILE, path, xml_temp)  
                fab_logpath = get_xml_value(nodes[0], 'LogFolder')
                burn_engine_type = get_xml_value(nodes[0], 'BDBurnEngineType')
                tempfolder_path = get_xml_value(nodes[0], 'TempFolder')  
    else:
        if project.upper() == 'DVDFAB 8' or project.upper() == 'DVDFAB8':
            for path in path_list:
                tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp)
                fab_logpath = get_xml_value(nodes[0], 'LogFolder')
                burn_engine_type = get_xml_value(nodes[0], 'BurnEngineType')
                tempfolder_path = get_xml_value(nodes[0], 'TempFolder')	
        else:
            for path in path_list:
                tree, nodes = myxml.read_xml(XML_FILE, path, xml_temp) 
                fab_logpath = get_xml_value(nodes[0], 'LogFolder')
                burn_engine_type = get_xml_value(nodes[0], 'BDBurnEngineType')
                tempfolder_path = get_xml_value(nodes[0], 'TempFolder')				
                           
    dest_path = tempfolder_path if '.ISO' == os.path.splitext(res[6].upper())[1] else dest_path
    initlog('before running, dest_path is: %s' % dest_path)    
    tempfolder_path = ''.join((tempfolder_path, 'ReportCrash')).replace("_nbsp;"," ")
    fab_logpath = fab_logpath.replace("_nbsp;"," ")
    initlog("fab_logpath is: %s; tempfolder_path is: %s" %(fab_logpath, tempfolder_path))
    logpath = (fab_logpath, tempfolder_path)         
    remove_fab_logfile(fab_logpath)
    return dest_path, logpath, burn_engine_type


def update_session_before_running(pc_name, src_iso_path, res):             
    start = time.mktime(time.localtime())
    Start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    src_iso_path = src_iso_path.replace('\\','\\\\')  
    update_flag = update_session_table(res, 1, res[0], res[1], pc_name, src_iso_path, Start_time) 
    return start, Start_time, src_iso_path, update_flag

  
def change_fuhao(file_path):
    return file_path.replace('/','\\') if os.name == "nt" else file_path.replace('\\','/')
   

def kill_DVDFab_process(dest_path, index):
    """ 检测Win下的进程，如果存在则直接杀死 """
    result = ''
    process_list = ["DVDFab.exe", "WerFault.exe", "dwwin.exe", "FabReport.exe"]
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
    result = "no process exists; " if result == "" else result
    initlog("kill DVDFab process: %s" % result)
    return result


def kill_mac_DVDFab_process(dest_path, index):
    """ 检测Mac下的进程，如果存在则直接杀死 """
    result = ''
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
    result = "no process exists; " if result == "" else result
    initlog('kill mac DVDFab process result:  %s' % result)
    return result


def check_process(process_name):
    """ 检测Mac下的进程 """
    cmd = 'ps -ef | grep %s' % process_name
    f = os.popen(cmd)
    regex = re.compile(r'\w+\s+(\d+)\s+.*')
    txt = f.read()
    return  txt
    
    
def kill_process_name(process_name):
    """ 强行杀死进行 """
    os.system('killall %s' % process_name)
	
def get_dest_path(path):
    """ 获取每个客户端的存放运行结果的目的路径 """
    dest_path = change_fuhao(path)
    dest_path = os.path.split(dest_path)[0] if '.ISO' == os.path.splitext(dest_path.upper())[1] else dest_path
    return dest_path
	
	
def get_case_end_info(start, dest_path):
    """在case结束的时候，计算下结束时间，整个运行过程所需时间，以及最后的目录的大小"""
    end = time.mktime(time.localtime())
    End_time = time.strftime('%Y-%m-%d %H:%M:%S')
    Total_time = int(str(end-start).split('.')[0])
    Total_time = str(Total_time/3600)+':'+str(Total_time%3600/60)+':'+str(Total_time%3600%60%60) 	
    Folder_size = '%.2lf' % (get_Filesize(dest_path)/1024.0/1024.0)
    initlog('the terminal Folder_size: %s' % str(Folder_size)) 
    return End_time, Total_time, Folder_size
    
    
def running(pc_name, res, client_dest_path, DVDFab_path, params_dict, XML_FILE):
    """  """     
    start = Start_time = dest_path = result = logpath = burn_engine_type = ''
    update_registry_value(res, params_dict["project"], XML_FILE)          
    module, iso,ripper_mode = res_to_iso(res)       
    src_iso_path = search_iso_path(module, iso, params_dict["bd_path"], params_dict["dvd_path"], \
	params_dict["file_path"],params_dict["bd_path_mac"],params_dict["dvd_path_mac"],params_dict["file_path_mac"])  
    update_flag = False      
    
    if src_iso_path:  
        DVDFab_path_cmd_string, dest_path = get_cmd_string(res, DVDFab_path, src_iso_path, client_dest_path)
        dest_path, logpath, burn_engine_type = before_running(res, src_iso_path, dest_path, params_dict["project"], XML_FILE)
        start, Start_time, src_iso_path, update_flag = update_session_before_running(pc_name, src_iso_path, res) 
        if not update_flag:
            result = ' Auto_test_tool raise error;'
            update_session_table(res,3,res[0],res[1],pc_name,src_iso_path = '',Start_time = '',End_time = '',Total_time = '',Folder_size = '',result = result) #Auto_test_tool
            initlog('update Flag to 3; Auto_test_tool raise error')  
            return  start, Start_time, dest_path, src_iso_path, result, logpath, burn_engine_type, update_flag  
        		
        result = start_running(res, DVDFab_path_cmd_string, module, ripper_mode, dest_path, params_dict["bd_analysis_time"], params_dict["bd_interval_time"], \
		params_dict["bd_ripper_analysis_time"], params_dict["bd_ripper_interval_time"],params_dict["dvd_analysis_time"], params_dict["dvd_interval_time"], \
		params_dict["file_analysis_time"], params_dict["file_interval_time"], burn_engine_type, client_dest_path)      
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
    return socket.gethostbyname(socket.gethostname()) if os.name == "nt" else ip_address('ipv6').split(";")[0]


def ipv4_address():
    return socket.gethostbyname(socket.gethostname()) if os.name == "nt" else ip_address('ipv4').split(";")[0]
   

def get_new_file_ctime_macos(path):
    """ 获取指定目录下的最新的以fab_config开头的文件 """
    file_list = []
    ctime_list = []
    file_ctime_list = []
    fab_config_file_list = []
    for onefile in os.listdir(path):
        if onefile.upper().startswith('CONFIG'):
            path_file= os.path.join(path, onefile)
            if os.path.isdir(path_file):
                file_list.append(path_file)
                ctime_list.append(os.stat(path_file).st_ctime)

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
    """ 获取指定目录下的最新的以fab_config开头的文件 """
    c_time = 0
    xml_file = ""
    for onefile in os.listdir(path):
        if onefile.startswith('fab_config'):
            path_file= os.path.join(path, onefile)
            if os.path.isfile(path_file):
                cur_c_time = os.stat(path_file).st_ctime
                if cur_c_time > c_time:
                    c_time = cur_c_time
                    xml_file = path_file
    return xml_file
                    
#不再使用	
def get_new_file_ctime_windows_old(path):
    file_list = []
    ctime_list = []
    for onefile in os.listdir(path):  
        if onefile.upper().startswith('FAB_CONFIG'):
            path_file= os.path.join(path, onefile)
            if os.path.isfile(path_file):
                file_list.append(path_file)
                ctime_list.append(os.stat(path_file).st_ctime)
  
    XML_FILE = file_list[ctime_list.index(max(ctime_list))] if ctime_list else ""
    return XML_FILE
	
	
def get_node_value(node, key):
    """ 获得xml文档的节点的值 """
    try:
        value = node.attrib[key]
    except Exception, e:
        value = ""
        initlog('xml file analyze error; %s' % str(e))
    return value
	
def get_DVDFab_path(XML_FILE):
    """ 获取DVDFab的安装路径 """
    if os.name == 'nt': 
		tree, nodes = windows_xml.read_xml(XML_FILE, 'common_setting', xml_temp)
		DVDFab_path = get_node_value(nodes[0], 'Path')
    else:
		DVDFab_path = DVDFAB_PATH
    return DVDFab_path
	
	
def get_case_info(res):
    """ 获得case的信息 """
    #case_id, case_num, case_dest_path
    return res[0], res[1], res[6]
	
	
def operate_file(logpath, case_id, Start_time, dest_path):
    """ case跑完之后操作文件：包括获取log文件，上传log文件，拷贝以及压缩log文件 """
    start_time = Start_time.replace('-','_').replace(':','_').replace(' ','_')
    log_filename_list = get_log_files(logpath)      
    upload_file(log_filename_list, case_id)        
    copy_file(log_filename_list, dest_path)       
    zip_files(log_filename_list, dest_path + '/' + start_time +'.zip')
   
def main(): 
    initlog("\n\n**************************begin**************************")
    pc_name = get_pcname()         
    pc_ip = ipv4_address()
    _, client_dest_path = get_client_path(pc_ip)
    client_dest_path = change_fuhao(client_dest_path)  
    initlog("client_dest_path is : %s" % client_dest_path)	
    params_dict = read_ini(INI_FILE)    
    XML_FILE = get_new_file_ctime_windows(windows_xml.XML_FILE_PATH) if os.name == "nt" else get_new_file_ctime_macos(myxml.XML_FILE_PATH)
    if not XML_FILE:
        initlog("xudedong ,does not find %s" % XML_FILE)
        return	
    initlog("current xml file is: %s" % XML_FILE)
    DVDFab_path = get_DVDFab_path(XML_FILE)
    if DVDFab_path:  
        initlog("find DVDFab path: %s" % DVDFab_path)
        records = get_all_cases(pc_name)
        if not records:
            initlog('sorry , does not have any case for you;\n')        
            return 
        for res in records:
            initlog("\n\n+++++++++++++++++++++++++++++++++     %d    +++++++++++++++++++++++++++++++++++++++++" % (records.index(res) + 1))
            case_id, case_num, case_dest_path = get_case_info(res)
            initlog("this is the %d case to run, CASE ID is %s" % (records.index(res) + 1, case_id))
            start,Start_time,dest_path,src_iso_path,result,logpath,burn_engine_type, update_flag = running(pc_name,res,client_dest_path,DVDFab_path,params_dict, XML_FILE) 
            if start == '' or update_flag == False: 
				update_session_table(res, 3, case_id, case_num, pc_name, result = result)       #does not find iso;
				initlog('update Falg to 3;  the session table does not update before running11111111111111\n')             
            else:          
                dest_path = get_dest_path(case_dest_path)
                initlog("dest_path is : %s" % dest_path)	
                process_result = kill_DVDFab_process(dest_path, case_id) if os.name == 'nt' else kill_mac_DVDFab_process(dest_path, case_id)
                result = process_result if result == '' else result 	
                End_time, Total_time, Folder_size = get_case_end_info(start, dest_path)	
                result += judge_filesize(res, Folder_size)				
                update_flag = update_session_table(res, 2, case_id, case_num, pc_name, src_iso_path, Start_time, End_time, Total_time, Folder_size, result)
                operate_file(logpath, case_id, Start_time, dest_path)							
	else:
		result = 'not find Fab path\n\n'
		update_session_table(res, 3, case_id, case_num, pc_name, result = result)
		initlog("update Flag to 3; %s" % result)  


if __name__ == '__main__':
    main()
    print 'ok, this is end! This window will be closed after 5 seconds!!'  
    time.sleep(5)	
    
    
 
 
 
