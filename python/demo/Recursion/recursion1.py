#-*- encoding:utf-8 -*-

li = [1,[[2,[3,4]],[5,[6,7,[8,9]]]]]

def print_list(lis):
    for i in lis:
        if isinstance(i, list):
            print_list(i)
        else:
            print i

#假设left和right方法已经存在
def ins(lis):
    if not lis.left and not lis.right:
        print lis
    else:
        if lis.left:
            ins(lis.left)
        if lis.right:
            ins(lis.right)
        print ins


def digui(n):
    sum = 0
    if n<=0:
        return 1
    else:
        return n*digui(n-1)
 


        
if __name__ == "__main__":
    print_list(li)
    print(digui(5))
    
