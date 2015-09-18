#-*- encoding:utf-8 -*-
"""
    该脚本的主要作用就是输出指定的起始日期和截止日期中间的所有日期，但是日期格式要求为：xxxx-xx-xx.
    以后可以支持多种格式的日期形式
"""

import re
import sys

start_time = "2011-12-27"
end_time = "2013-01-02"
#month = [i for i in xrange(1,13)]
#day = [i for i in xrange(1,32)]

def get_range_day_end(year, month):
    if month in [1,3,5,7,8,10,12]:
        range_day_end = 32
    elif month in [4,6,9,11]:
        range_day_end = 31
    elif month == 2:
        if (str(year).endswith("00") and year % 400 == 0) or (not str(year).endswith("00") and year % 4 == 0):
            range_day_end = 30
        else:
            range_day_end = 29
    return range_day_end

def format_month_or_day(month_or_day):
    if month_or_day < 10:
        month_or_day = "0" + str(month_or_day)
    else:
        month_or_day = str(month_or_day)
    return month_or_day

def get_day(start_time,end_time,year, month, range_day_start,range_day_end):
    for each_day in xrange(range_day_start,range_day_end):
        each_day = format_month_or_day(each_day)
        output_date = str(year) + "-" + month + "-" + each_day
        if start_time <= output_date <= end_time:
            print output_date

def format_time(start_time,end_time):
    pattern = "^\d{4}-\d{2}-\d{2}$"
    #print re.findall(pattern,start_time)
    #print re.findall(pattern,end_time)
    if not re.findall(pattern,start_time) or not re.findall(pattern,end_time):
        print "format error, only support xxxx-xx-xx"
        return
    start_year = int(start_time.split("-")[0])
    start_month = int(start_time.split("-")[1])
    start_day = int(start_time.split("-")[2])
    end_year = int(end_time.split("-")[0])
    end_month = int(end_time.split("-")[1])
    end_day = int(end_time.split("-")[2])

    #当年份不同的时候(截止年份大于起始年份)
    if end_year > start_year:
        #先把开始年的起始日期到最后一天的日期打印出来
        for each_month in xrange(start_month, 13):
            range_day_end = get_range_day_end(start_year, each_month)    
            each_month = format_month_or_day(each_month)
            get_day(start_time,end_time,start_year, each_month, 1,range_day_end)
            
        #中间的年份日期循环就可以了            
        for each_year in xrange(start_year + 1, end_year):
            print each_year
            for each_month in xrange(1, 13):
                range_day_end = get_range_day_end(each_year, each_month)    
                each_month = format_month_or_day(each_month)
                get_day(start_time,end_time,each_year, each_month, 1 ,range_day_end)
                
         #把最后一年的日期从1月1号到截止日期打印出来       
        for each_month in xrange(1, end_month + 1):
            range_day_end = get_range_day_end(end_year, each_month)    
            each_month = format_month_or_day(each_month)
            get_day(start_time,end_time,end_year, each_month, 1 ,range_day_end)
            
    #年份相同的时候(截止年份等于起始年份) 
    elif end_year == start_year:
        #月份不同的时候
        if end_month > start_month:
            for each_month in xrange(start_month, end_month + 1):
                range_day_end = get_range_day_end(start_year,each_month)    
                each_month = format_month_or_day(each_month)
                get_day(start_time,end_time,start_year, each_month, 1 ,range_day_end)
                
        #月份相同的时候
        elif end_month == start_month:
            if end_day >= start_day:
                range_day_end = get_range_day_end(start_year,start_month)
                start_month = format_month_or_day(start_month)
                get_day(start_time,end_time,start_year, start_month, start_day ,range_day_end)
            else:
                print "截止日期小于起始日期，请重新输入。日期有错误"
                
        else:
            print "截止日期小于起始日期，请重新输入。月份有错误"
            
    #(截止年份小于起始年份)    
    else:
        print "截止日期小于起始日期，请重新输入。年份有错误"

if __name__ == "__main__":
    format_time(start_time,end_time)
    #format_time(sys.argv[1],sys.argv[2])
