#if 1 == True:
if 1:
    print 11111111
#if 0 == False:
if 0:
    print 22222222

li = ["a", "c", "b", "c", "a", "a", "b"]

dict = {}
new_li = []
li_totals = []

for i in li:
    if i not in new_li:
        li_totals.append((i, li.count(i)))
        new_li.append(i)
        dict[i] = li.count(i)


print dict
print new_li
print li_totals
