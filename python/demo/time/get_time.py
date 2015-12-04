import time, datetime
def get_time():
    t1 = time.localtime()#current date
    t2=datetime.datetime(t1[0],t1[1],t1[2],t1[3],t1[4],t1[5])   
    t3=t2-datetime.timedelta(days=1)
    t3=str(t3)
    print type(t3)
    return t3

get_time()
