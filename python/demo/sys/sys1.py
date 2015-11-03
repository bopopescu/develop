import sys
print type(sys.path)

for i in sys.path:
    print i


import test
print test.add
test.add()
