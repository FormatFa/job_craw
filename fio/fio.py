import logging


def readstring(file,enconding='UTF-8'):
    with open(file,"r",encoding=enconding) as fp:
        strw = fp.read()
        return strw
def writestring(file,strw,encoding='UTF-8'):
    with open(file,"w",encoding=encoding) as fp:
        fp.write(strw)