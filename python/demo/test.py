m = 10
n = 1
left = []

while 1:
    if len(left) == 1 and left[0] % 3 != 0:
        break
    last = left[-1] if left else 0
    del left[:]
    left = [i for i in xrange(last+1, last+m+1) if i%3!=0]
    n += 1
    m = len(left)
print left











"""
start = 100
end = 1

list_3 = []

while 1:
    if list_3 and list_3
"""
