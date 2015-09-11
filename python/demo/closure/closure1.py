def hellocounter(name):
    count = [0]
    def counter():
        print 99999999
        count[0] += 1
        print 'Hello, ', name, ',', str(count[0]) , ' access!'
    return counter


hello = hellocounter("mas12")

print hello
hello()
hello()
hello()


