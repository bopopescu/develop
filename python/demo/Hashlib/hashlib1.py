#-*- encoding:utf-8 -*-
'''
Created on 2016年9月21日

@author: dedong.xu
'''

import hashlib
mystr = "xdd"


class EncryptionAlgorithm(object):
    """ python常用的加密算法 """
    
    def __init__(self, mystr):
        self.mystr = mystr
        
    def get_md5(self):
        """ 使用md5加密 """
        return hashlib.md5(self.mystr).hexdigest()
    
    def get_sha1(self):
        """ 使用sha1加密 """
        return hashlib.sha1(self.mystr).hexdigest()
    
    def get_sha224(self):
        """ 使用sha224加密 """
        return hashlib.sha224(self.mystr).hexdigest()
    
    def get_sha256(self):
        """ 使用sha256加密 """
        return hashlib.sha256(self.mystr).hexdigest()
    
    def get_sha384(self):
        """ 使用sha384加密 """
        return hashlib.sha384(self.mystr).hexdigest()
    
    def get_sha512(self):
        """ 使用sha512加密 """
        return hashlib.sha512(self.mystr).hexdigest()


if __name__ == "__main__":
    ea = EncryptionAlgorithm(mystr)
    print ea.get_md5()
    print ea.get_sha1()
    print ea.get_sha224()
    print ea.get_sha256()
    print ea.get_sha384()
    print ea.get_sha512()
