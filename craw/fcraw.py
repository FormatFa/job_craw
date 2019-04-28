import requests
from urllib.parse import quote,unquote
from config import crawconfig
import os
import logging
import requests
from fio.fio import *
import  hashlib
clog=logging.getLogger("craw")

clog.setLevel(logging.INFO)

hash = hashlib.md5()


# xpath查找到的结果是个列表,但是大多数情况我们只要第一个,每一个都判断长度的话,代码会很多余,这个函数就是提取出第一个,default可以指定默认值
def getXpathValue(l,default=''):
    if len(l)==1:
        return l[0]
    else:
        return default



class Craw():
    def __init__(self):
        self.outdir = os.path.join(self.getsavedir(), self.getSite())
        pass
    # 带检查的打开文件，如果文件有内容，时不想覆盖文件
    def getoutdir(self):
        return os.path.join(self.getsavedir(), self.getSite())
    def getSite(self):
        return "example"

    def getJobPath(self):

        return os.path.join(self.outdir, self.getSite() + "_job.txt")

    def getCompanyPath(self):
        return  os.path.join(self.outdir, self.getSite() + "_company.txt")

    def fopen(self,file, mode='r', encoding="UTF-8",auto_mkdir=False):


        if  crawconfig.mode!='dev' and  os.path.exists(file) and os.path.getsize(file)!=0:
            raise Exception("{} 已经存在且长度不是0 ".format(file))
        if auto_mkdir and not os.path.exists(os.path.split(file)[0]):
            clog.info("mk parent dir for :{}".format(file))
            os.makedirs(os.path.split(file)[0])
        return open(file,mode=mode,encoding=encoding)

    def getheaders(self):
        return {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Fire"}
    # 这里的get，添加一个缓存,

    def getText(self,url,params=None,**kwargs):
        if url=='':
            return None
        ha = hash.update(url.encode())
        cachepath = os.path.join( crawconfig.cachedir ,hash.hexdigest()+".html" )
        if os.path.exists(cachepath):
            clog.info("read {} from cache..".format(cachepath))
            return readstring(cachepath)

        res=requests.get(url,params=params,**kwargs)

        # 请求成功才会缓存
        if res.status_code==200:

            clog.info("add {} from cache..".format(cachepath))
            writestring(cachepath,res.text)

        else:
            return None
        return res.text

    def getkeyword(self):
        return quote( "大数据")

    def getsavedir(self):
        dire= crawconfig.outdir
        if not os.path.exists(dire):
            clog.info("mkdir for output:",dire)
            os.makedirs(dire)
        return dire

