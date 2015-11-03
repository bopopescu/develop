#-*- encoding:utf-8 -*-

import re

def pythonReSubDemo():
    """
        demo Pyton re.sub
    """
    inputStr = "hello 123 world 456";
    
    def _add111(matched):
        print matched.group()
        intStr = matched.group("number"); #123
        print intStr
        intValue = int(intStr);
        addedValue = intValue + 111; #234
        addedValueStr = str(addedValue);
        print addedValueStr,11111111111111
        return addedValueStr;
        
    replacedStr = re.sub("(?P<number>\d+)", _add111, inputStr);
    print "replacedStr=",replacedStr; #hello 234 world 567


if __name__=="__main__":
    pythonReSubDemo();





