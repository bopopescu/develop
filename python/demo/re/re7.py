#-*- encoding:utf-8 -*-

import re
def test():
    inputStr = "hello 123 world 456";
    def add(params):
        print "params: ", params
        intStr = params.group()
        print "group result: ", intStr
        strValue = str(int(intStr) + 111)
        return strValue
    replacedStr = re.sub("(?P<number>\d+)", add, inputStr);
    print "***********************************************"
    print "final result: ", replacedStr



if __name__ == "__main__":
    test()
