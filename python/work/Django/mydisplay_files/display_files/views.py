# coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import os, time
#import chardet
from django.utils.http import urlquote
from xml.etree import ElementTree
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#sys.setdefaultencoding( "gbk" )
#sys.setdefaultencoding( "ascii" )

ROOT = 'D:/shared'
PATH = '/develop/'

def develop(request):
    name_list = []
    dirs_list = []
    files_list = []
    context_list = []
    dir_content_list = []
    content = ''
    url = request.path
    if url.endswith('/'):     
        url1 = os.path.split(url)[0]
    else:
        url1 = url
    url2 = os.path.split(url1)[0] + '/'
    dir_name = os.path.split(url1)[1]
    if os.path.isdir(ROOT + url1):
        files = os.listdir(ROOT + url1)
        for filename in files:
            if os.path.isdir(os.path.join(ROOT + url1, filename)):   
                dir_file = os.path.join(ROOT + url1, filename)
                st = os.stat(dir_file)
                year = time.localtime(st.st_mtime)[0]
                mon = time.localtime(st.st_mtime)[1]
                day = time.localtime(st.st_mtime)[2]
                hour = time.localtime(st.st_mtime)[3]
                min = time.localtime(st.st_mtime)[4]
                sec = time.localtime(st.st_mtime)[5]
                if min < 10:
                    min = '0' + str(min)
                if sec < 10:
                    sec = '0' + str(sec)
                modify_time = str(year) + '/' + str(mon) + '/' + str(day) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec)
                dirs_list.append((filename, modify_time))
            else:
                if filename.endswith('.xml'):
                    path_file = os.path.join(ROOT + url, filename)   
                    f = open(path_file, 'r')
                    content = f.read()
                    f.close()
                    all_codes = ['ascii','utf-8','gb2312', 'gbk']
                    for code in all_codes:
                        try:                      
                            if code.upper() == 'UTF-8':   
                                pass
                            else: 
                                content = content.decode(code).encode('UTF-8')
                                content = content.replace('encoding='+code, 'encoding="UTF-8"')
                            root = ElementTree.fromstring(content)
                            node_name = root.findall('name')               
                            node_context = root.findall('description')
                        except:
                            pass
                    for name in node_name:
                        name_list.append(name.text.strip())
                    node_context = root.findall('description')
                    for context in node_context:
                        context_list.append(context.text.strip())
                    dir_content_list = zip(name_list, context_list)  
                else:
                    path_file = os.path.join(ROOT + url, filename)
                    st = os.stat(path_file)
                    year = time.localtime(st.st_mtime)[0]
                    mon = time.localtime(st.st_mtime)[1]
                    day = time.localtime(st.st_mtime)[2]
                    hour = time.localtime(st.st_mtime)[3]
                    min = time.localtime(st.st_mtime)[4]
                    sec = time.localtime(st.st_mtime)[5]
                    if min < 10:
                        min = '0' + str(min)
                    if sec < 10:
                        sec = '0' + str(sec)
                    modify_time = str(year) + '/' + str(mon) + '/' + str(day) + ' ' + str(hour) + ':' + str(min) + ':' + str(sec)
                    files_list.append((filename, modify_time))
        all_list = str(dirs_list + files_list)
        dirs_str = str(dirs_list)
        full_path = ROOT + url
        dict = {'request':request,
                'dirs_list':dirs_list,
                'files_list':files_list,
                'content':content,
                'url':url,
                'url2':url2,
                'dir_name':dir_name,
                'name_list':name_list,
                'dir_content_list':dir_content_list,
                'PATH':PATH,
                'all_list':all_list,
                'dirs_str':dirs_str,
                'full_path':full_path
                }
        return render_to_response('develop.html',dict)
    else:
        file_name = ROOT + url1
        f=open(file_name, 'rb')
        data=f.read()
        f.close()
        file_name = os.path.split(url1)[1]
        response = HttpResponse(data,content_type='application/octet-stream') 
        response['Content-Disposition'] = 'attachment; filename=%s' % urlquote(file_name)
        return response
    

