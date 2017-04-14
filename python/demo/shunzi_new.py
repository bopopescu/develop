#-*- encoding:utf-8 -*- 

l = [1,2,3,5,6,7,8,9,10,11,13,14,15,16,17]

curL = [l[0]]
maxL = [l[0]]
start = end = 0

for i in xrange(len(l)-1):
    if abs(l[i]-l[i+1]) == 1:
        curL.append(l[i+1])
        end = i+1
        continue
		
    if len(curL) > len(maxL):
        maxL = curL
        curL = [l[i+1]]
        start = i+1

if len(curL) > len(maxL):
    maxL = curL

print maxL
print start, end
