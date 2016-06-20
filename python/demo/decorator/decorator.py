import time

def deco(func):
    print 11111111111
    def wrapper(*args, **kwargs):
        print 2222222222
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print end - start
    return wrapper

@deco
def test(a,b,c,f):
    time.sleep(.1)


if __name__ == "__main__":
    test(1,2,3,4)
