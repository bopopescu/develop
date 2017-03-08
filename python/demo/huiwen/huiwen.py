#-*- encoding:utf-8 -*-
'''
Created on 2017-1-16

@author: dedong.xu

@description: python判断回文的几种方法
'''

strs = "12345754321"
strs = "123456789"*5 + "987654321"*5

def isHuiWen(strs):
    if len(strs) % 2 ==0:
        mid_before = len(strs)/2
        mid_after = mid_before
    else:
        mid_before = (len(strs)-1)/2
        mid_after = mid_before + 1
    front = strs[0:mid_before]
    end = strs[mid_after:][::-1]
    print front
    print end
    if front == end:
        print "是回文"
    else:
        print "不是回文"
        
def isHuiWen1(strs):
    if len(strs) % 2 !=0:
        strs = strs.replace(strs[len(strs)/2], "")
    length = len(strs)
    print strs[:length/2], strs[length/2:][::-1]
    if strs[:length/2] == strs[length/2:][::-1]:
        print "回文"
    else:
        print "不是回文"
        
        
def isHuiWen2(strs):
    length = len(strs)
    if length % 2 == 0:
        front = strs[:length/2]
        end = strs[:length/2-1:-1]
    else:
        front = strs[:length/2]
        end = strs[:length/2:-1]
    if front == end:
        print "回文"
    else:
        print "不是回文"
        
#strs = "asdfdsa"        
def isHuiWen3(strs):
    length = len(strs)
    flag = True
    for i in xrange(0, (length/2)):
        if strs[i] == strs[length-1-i]:
            print i, length-1-i, strs[i], strs[length-1-i]
        else:
            flag = False
            break
    if flag:
        print "是回文"
    else:
        print "不是回文"

def isHuiWen4(s):
    for i in range(len(s)/2):
        if not s[i] == s[len(s)-i-1]:
            return False
    return True

def isHuiWen5(s):
    return s == s[::-1]


def num():
    li = [1,2,3,4]
    n = 0
    for i in li:
        for j in li:
            for k in li:
                if i != j and j != k and i != k:
                    print "%d %d %d" %(i,j,k)
                    n+=1
    print n, "aaaaaaaaaaaa"
    
    
def cur_days(date):
    import re, sys
    date = raw_input("请输入年份,格式为2016-05-12: ")
    p = r"\d{4}-\d{1,2}-\d{1,2}"
    if re.match(p, date.strip()):
        year, month, day = date.split("-")
        if int(month) > 12:
            print "月份不对"
            sys.exit()
        elif int(day) > 31:
            print "日期不对"
            sys.exit()
        day_dict = {0:0, 1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        
        shang = 400 if year.endswith("00") else 4
        run = True if int(year)%shang == 0 else False
        if run:
            day_dict[2] = 29
        t = 0
        for i in xrange(int(month)):
            t += day_dict[i]
            #print day_dict[i]
        t+=int(day)
        print t
    else:
        print "格式不对"
        sys.exit()

    
    
def print_c(row, indent):
    t = ""
    flag = True
    for i in xrange(row/2):
        if flag:
            t+= "  "*(indent+row/2-i) + "* *\n"
            flag = False
        else:
            t+= "  "*(indent+row/2-i) + "*\n"
    print t.rstrip()
    r = ""
    for i in xrange(row+1, row/2,-1):
        r+= "  "*(indent+row+1-i) + "*\n"
    print r.rstrip() + " *"
      
   
      

if __name__ == "__main__":  
    #isHuiWen(strs)  
    #isHuiWen1(strs)
    #isHuiWen2(strs)
    #isHuiWen3(strs)
    #isHuiWen4("asdfgfdsa")
    #print strs
    #print isHuiWen5(strs)
    #num()
    #cur_days("2012-02-12")
    print_c(9, 0)

