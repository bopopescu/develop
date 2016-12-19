#-*- encoding:utf-8 -*-

'''
Created on 2016-12-16

@author: dedong.xu

@description: 模拟http post请求上传文件的几种方法
'''
postfile = "urllib_post.py"
url = "http://10.10.2.64:9001/upload_file_test/"
    
def curl_post_file(url, postfile):
    """ curl上传文件 """
    import pycurl
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    #c.setopt(c.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
    c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, postfile))])
    c.perform()
    c.close()
    
   
def curl_post_file2(url, postfile):
    """ curl上传文件 """
    import StringIO 
    import pycurl
    storage = StringIO.StringIO()
    c = pycurl.Curl()
    values = [("file", (c.FORM_FILE, postfile)),]
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.setopt(c.HTTPPOST, values)
    c.setopt(c.VERBOSE, 1)    #打印上传过程中的信息
    c.perform()
    c.close()
    content = storage.getvalue()
    print content
    
def post_file(url, postfile):
    """ poster模块和urllib2模块上传文件 """
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
    import urllib2
    params = {"file": open(postfile, "rb")}
    register_openers()          
    #opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    datagen, headers = multipart_encode(params)
    # Create a Request object
    request = urllib2.Request(url, datagen, headers)    
    # Actually do POST request
    response = urllib2.urlopen(request)
    result = response.read() 
    response.close()   
    print result  
     
    
def post_file2(url, postfile):
    """ poster模块和urllib2模块上传文件，带有cookie """
    import cookielib 
    import urllib2
    from poster.encode import multipart_encode
    from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler
    cj = cookielib.CookieJar()
    handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), *handlers)
    urllib2.install_opener(opener)
    params = {'file': open(postfile, "rb")}
    data, headers = multipart_encode(params)
    req = urllib2.Request(url, data, headers)
    result = urllib2.urlopen(req).read()
    print result    
    
if __name__ == "__main__":
    #curl_post_file(url, postfile)
    #curl_post_file2(url, postfile)
    #post_file(url, postfile)
    post_file2(url, postfile)
    