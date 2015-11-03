#-*- encoding:utf-8 -*-

import re

def test():
    s1 = "helloworld, I am 30!"
    w1 = "world"
    m1 = re.search(w1, s1)

    print m1
    if m1:
        print "find: ", m1.group()

    if re.match(w1, s1) == None:
        print "can not find match"

    w2 = "helloworld"
    m2 = re.match(w2,s1)
    if m2:
        print "match: ", m2.group()

if __name__ == "__main__":
    test()
