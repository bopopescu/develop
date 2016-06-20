list1 = [6,4,3,3,3,1,2,8,11,12,13,35,23,34,36,37,38,80]


new_list = sorted([i for i in set(list1)])
print new_list
print "*"*50
index = 0
di = {}

shunzi_list = []

while index <= len(new_list)- 2 and len(new_list) > 1:
    shunzi_list.append(new_list[index])
    if index == len(new_list) - 1:
        if new_list[-1] - new_list[-2] == 1:
            pass
        else:
            shunzi_list.append(new_list[-1])
    
    if new_list[index + 1] - new_list[index] == 1:   
        index += 1
    else:
        di[index] = shunzi_list
        index += 1
        shunzi_list = []   
   

#print di


for i in di:
    print i, di[i]



        
        
        
