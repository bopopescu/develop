#-*- encoding:utf-8 -*-

"""
    上传文件到亚马逊云上
"""

import os
import time
import datetime
import zipfile

import boto3

BASE_DIR = "."
bucket = ""

def get_yesterday():
    """ 获得昨天的日期 """
    t1 = time.localtime()#current date
    t2 = datetime.datetime(t1[0],t1[1],t1[2])   
    t3 = t2-datetime.timedelta(days = 1)
    yesterday = str(t3)[:-9].replace("-", "")
    return yesterday

def get_the_day(day, n):
    """ 根据给定的日期，获得相应的日期 """
    timestamp = time.strptime(day, "%Y/%m/%d")
    int_timestamp = int(time.mktime(timestamp))
    dateArray = datetime.datetime.utcfromtimestamp(int_timestamp)
    ago = dateArray + datetime.timedelta(days = n)
    str_date = ago.strftime("%Y/%m/%d")
    return str_date

def uploadFile(localfile, remotefile):
    """ 上传文件 """
    data = open(localfile, "rb")
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).put_object(Key = remotefile, Body = data)
    data.close()

class UploadFileToAws(object):
    """ 使用python的第三方模块boto3来上传文件至亚马逊云 """

    def __init__(self, localfile, remotefile, bucket):
        """ 初始化变量 """
        self.localfile = localfile
        self.remotefile = remotefile
        self.bucket = bucket
        self.data = open(self.localfile, "rb")
        self.s3 = boto3.resource("s3")

    def upload(self):
        """ 上传文件至亚马逊云 """
        self.s3.Bucket(self.bucket).put_object(Key = self.remotefile, Body = self.data)
    
    def download(self):
        """ 从亚马逊云上下载文件 """
        self.s3.Bucket(self.bucket).download_file(self.remotefile, "aaa.zip")#self.localfile)


    def close(self):
        """ 关闭文件句柄 """
        self.data.close()


class ZipFile(object):
    """ 使用python的zipfile模块来压缩文件 """

    def __init__(self, zipfilename, mode = "w"):
        """ 初始化变量 """
        self.zipfilename = zipfilename
        self.mode = mode
        self.zf = zipfile.ZipFile(self.zipfilename, self.mode, compression = zipfile.zlib.DEFLATED)

    def zipfile(self, filename):
        """ 压缩文件，向压缩包里写文件 """
        self.zf.write(filename)

    def close(self):
        """ 关闭文件对象 """
        self.zf.close()

def main(base_dir):
    yesterday = get_yesterday()
    year, month = yesterday[:4], yesterday[4:6]
    localfile = "%s.zip" % yesterday
    localpath = os.path.join(base_dir, yesterday)
    remotefile = "%s/%s/%s.zip" % (year, month, yesterday)
    zf = ZipFile(localfile)
    for eachfile in os.listdir(localpath):
        zf.zipfile(os.path.join(localpath, eachfile))
    zf.close()
    ufta = UploadFileToAws(localfile, remotefile, bucket)
    ufta.upload()
    ufta.download()
    ufta.close()
    #uploadFile(localfile, remotefile)

if __name__ == "__main__":
    main(BASE_DIR)

