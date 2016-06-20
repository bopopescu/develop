#-*- encoding:utf-8 -*-

"""ʹ��װ������װ���࣬ʹ���Ϊ����ģʽ"""

def Singleton(cls):
    instance = {}
    def _singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return _singleton
	
@Singleton	
class A(object):
    pass
	
a1 = A()
print id(a1)
a2 = A()
print id(a2)
print a1 == a2