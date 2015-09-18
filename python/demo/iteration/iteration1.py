#-*- encoding:utf-8 -*-
"""
    迭代序列，适用于元组和列表
"""
mytuple = (1,2,3,"ui","asd",789)

i = iter(mytuple)

print i.next()
print i.next()
print i.next()
print i.next()
print i.next()
print i.next()

print "************************"

#for loop
j = iter(mytuple)
for k in xrange(len(mytuple)):
    print j.next()
        
print "************************"

l = iter(mytuple)
while 1:
    try:
        print l.next()
    except StopIteration, e:
        print str(e)
        break
