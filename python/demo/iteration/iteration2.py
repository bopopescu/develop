#-*- encoding:utf-8 -*-
"""
    迭代字典，会遍历字典的key
"""

legends = {('poe','author'):(1809,1849,1976),('Gaudi','architect'):(1852,1906,1987),('Freud','psychoanalyst'):(1856,1939,1990)}

for eachlegend in legends.keys():
    continue
    print type(eachlegend), type(legends[eachlegend])
    print "Name: %s\tOccupation: %s" % eachlegend
    print "Birth: %s\tDeath: %s\tAlbum: %s\n" % legends[eachlegend]



for i in legends:
    print i,legends[i][0],legends[i][1],legends[i][2]
