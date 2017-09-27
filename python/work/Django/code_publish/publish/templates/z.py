class E(object):
    pass

class D(E):
    pass

class C(E):
    pass

class B(C, D):
    pass


class A(B):

    def __init__(self, value):
        self.__score = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("score must be integer")
        if value < 0 or value > 100:
            raise ValueError("score must between 0~100")
        self.__score = value

    @property
    def chazhi(self):
        return 100 - self.__score

a = A(12)
a.score = 60
print a.score

a.score = 9

print a.chazhi
print A.__mro__, type(A.__mro__)
for i in A.__mro__:
    print i.__name__, type(i.__name__)
