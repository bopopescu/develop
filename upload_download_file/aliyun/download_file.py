#-*- encoding:utf-8 -*-

"""
    用户输入相应的选项来选择下载哪些日期的文件
"""

import re
import sys
import oss2
import time
import datetime

accessKeyId = "";
accessKeySecret = "";
endpoint = "";
bucket_name = "";

def createBucket():
    """ 创建bucket """
    auth = oss2.Auth(accessKeyId, accessKeySecret)
    service = oss2.Service(auth, endpoint)
    print [b.name for b in oss2.BucketIterator(service)]
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
    return bucket

def downloadFile(bucket, remotefile, localfile):
    """ 下载文件 """
    try:
        bucket.get_object_to_file(remotefile, localfile)
    except Exception, e:
        pass

def color_print(msg, color='red', exits=False):
    """ 输出彩色字符串 """
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg
    if exits:
       time.sleep(2)
       sys.exit()
    return msg

def get_the_day(day, n):
    """ 根据给定的日期，获得相应的日期 """
    timestamp = time.strptime(day, "%Y/%m/%d")
    int_timestamp = int(time.mktime(timestamp))
    dateArray = datetime.datetime.utcfromtimestamp(int_timestamp)
    ago = dateArray + datetime.timedelta(days = n)
    str_date = ago.strftime("%Y/%m/%d")
    return str_date

def get_days_list(start_date, end_date):
    """ 获得给定的日期区间内的所有日期 """
    date_list = []
    n = 1
    while 1:
        str_date = get_the_day(start_date, n)
        date_list.append(str_date)
        n += 1
        if str_date < end_date:
            continue
        break
    return date_list


if __name__ == "__main__":
    color_print("请选择以下一种选项,您是要下载某一天的log还是要下载某以区间的log,1代表是某一天，2代表是某一区间")
    select = raw_input("请选择：")
    if select == "1":
        p = r"^(\d{4})/(\d{1,2})/(\d{1,2})$"
        while 1:
            date = raw_input("请输入日期,格式xxxx/xx/xx: ")
            re_com = re.search(p, date)
            if re_com:
                if int(re_com.group(2)) > 12:
                    print "月份有误,请重新输入"
                    continue
                if int(re_com.group(3)) > 31:
                    print "日期有误,请重新输入"
                    continue
                if date >= time.strftime("%Y/%m/%d"):
                    print "不能下载今天以及今天以后的文件，因为还没有上传"
                    continue
                date_list = [date]
                break
            else:
                print "格式不对,请重新输入"
    elif select == "2":
        p = r"^((\d{4})/(\d{1,2})/(\d{1,2}))-((\d{4})/(\d{1,2})/(\d{1,2}))$"
        while 1:
            date = raw_input("请输入日期区间,格式xxxx/xx/xx-xxxx/xx/xx: ")
            re_com = re.search(p, date)
            if re_com:
                start_date = re_com.group(1)
                end_date = re_com.group(5)
                if start_date > end_date:
                    print "起始日期不能大于截止日期,请重新输入"
                    continue
                else:
                    if int(re_com.group(3)) > 12:
                        print "起始日期月份不对,请重新输入"
                        continue
                    if int(re_com.group(4)) > 31:
                        print "起始日期不对,请重新输入"
                        continue
                    if int(re_com.group(7)) > 12:
                        print "截止日期月份不对,请重新输入"
                        continue
                    if int(re_com.group(8)) > 31:
                        print "截止日期不对,请重新输入"
                        continue
                    if end_date >= time.strftime("%Y/%m/%d"):
                        print "不能下载今天以及今天以后的文件，因为还没有上传"
                        continue
                    date_list = get_days_list(start_date, end_date)
                    break
            else:
                print "格式不对,请重新输入"
    else:
        print "没有这个选项，程序将退出"
        sys.exit(1)
    print "date list is: ", date_list
    bucket = createBucket()
    for date in date_list:
        src = date[:8] + date.replace("/", "") + ".zip"
        dst = date.replace("/", "") + ".zip"
        downloadFile(bucket, src, dst)
        #downloadFile(bucket, "2017/07/20170706.zip", "zz.zip")

