#-*- encoding:utf-8 -*-

import xmlrpclib

address = "http://10.10.2.170:9998"

def access_server():
    proxy = xmlrpclib.ServerProxy(address)
    result = proxy.analyze()
    print result
    return result



if __name__ == "__main__":
    access_server()
