from craw.fcraw import  Craw,getXpathValue
import logging
import os
import requests
from lxml import etree
import json
import re
clog=logging.getLogger("craw")
clog.setLevel(logging.DEBUG)




class WorkCrawFactory():
    def __init__(self):
        pass
    # 获取站点的处理,工厂模式
    @staticmethod
    def getSiteWorker(site):
        if site=="quanzhi":
            return quanzhi()

class liepin(Craw):
    def __init__(self):
        Craw.__init__(self)
        # https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=%E5%A4%A7%E6%95%B0%E6%8D%AE&init=-1&searchType=1&compkind=&fromSearchBtn=2&sortFlag=15&degradeFlag=0&jobKind=&industries=&clean_condition=&d_sfrom=search_prime&d_curPage=0&d_pageSize=40&curPage=1
        pass
        self.url='https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key={keyword}&init=-1&searchType=1&compkind=&fromSearchBtn=2&sortFlag=15&degradeFlag=0&jobKind=&industries=&clean_condition=&d_sfrom=search_prime&d_curPage=0&d_pageSize=40&curPage={page}'
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Fire"}
    def getSite(self):
        return 'liepin'

    def crawItem(self,page):

        res = self.getText(self.url.format(keyword= self.getkeyword(),page=page))
        clog.info("{} craw:{}",self.getSite(),page)

        html = etree.HTML(res)

        # 获取所有li,
        lis = html.xpath("//ul[@class='sojob-list']/li")

        # 提取出字段,
        for li in lis:
            job={}
            # 重新element
            # try:
            # clog.debug( etree.tostring(li).decode().strip())
            li2 = etree.HTML(etree.tostring(li))
            # 有一个标签是刚好 包含 很多信息的 如, 7-10万_上海_大专及以上_3年以上

            conditions=li2.xpath("//p[contains(@class,'condition')]/@title")[0].strip()
            title = li2.xpath("//div/div[1]/h3/a/text()")[0].strip()
            job_id = li2.xpath("//div/div[1]/h3/a/@href")[0].strip()
            company=li2.xpath('//div/div[2]/p[1]/a/text()')[0].strip()
            # /html/body/div[2]/div/div[1]/div[1]/ul/li[2]/div/div[2]/p[2]/span
            # 有些是有a标签,有些没有,直接string函数获取所有的文字
            company_index=li2.xpath('string(//div/div[2]/p[2]/span)').strip()
            refresh_date=li2.xpath('//div/div[1]/p[2]/time/text()')[0].strip()


            # 有些公司是点不进去的
            company_id=li2.xpath('//div/div[2]/p[1]/a/@href')
            company_id= company_id[0].strip() if len(company_id)==1 else ''



            conditions=conditions.split('_')

            job={
                "job_id": job_id,
                "title": title,
                "salary": conditions[0],
                "city": conditions[1],
                "work_year": conditions[3],
                "edu": conditions[2],
                "company": company,
                "company_index": company_index,
                # 这个网站没有
                "company_status":"",
                "refresh_date": refresh_date,

                "company_id": company_id,
                'desc':self.getJobDesc(job_id)

            }

            # print(job_id, title,salary,city,work_year,edu,company,company_id,company_index,company_status,refresh_date)


            job.update({"site": self.getSite()})

            print(page, job)
            self.jobfile.write(json.dumps(job, ensure_ascii=False))
            self.jobfile.write("\n")
    def getJobDesc(self,jobid):
        if not jobid.startswith("http"):
            jobid="https://www.liepin.com/"+jobid
        # print("get job desc:",jobid)
        strw = self.getText(jobid)

        if strw==None:
            print("job none",jobid)
            return
        # 正则表达式查找
        result = re.findall(r'<div class="content content-word">(.*?)(?<=div)', strw, flags=re.S)
        if len(result)>=1:
            result=result[0].replace(" </div",'').strip()
        else:
            result=''

        return result




    # 爬取工作
    def crawJob(self):
        self.jobfile = self.fopen(self.getJobPath(), "w", encoding="UTF-8",
                                  auto_mkdir=True)
        for i in range(0, 101):
            print("craw job page:"+str(i))
            self.crawItem(i)

        self.jobfile.close()

        pass
    def crawCompanyItem(self,company_url):

        clog.error("爬去公司:" + company_url)


        strw = self.getText(company_url, headers=self.headers)
        if strw==None:
            clog.error("return none:"+company_url)
            return

        html = etree.HTML(strw)
        # clog.debug(strw)
        # 查找不到可能是猎聘vip
        company_name = html.xpath('/html/body/div[2]/section/div/h1/text()')
        if company_name=='品友互动':
            raise Exception("fdsfsf")
        if len(company_name)!=1:
            clog.error("猎聘:获取公司名字失败:"+company_url)
            return
        company_name=company_name[0]


        company_summary=html.xpath("string(//div[@class='comp-summary-tag'])")



        regStatus = ""
        estiblishDate  = getXpathValue( html.xpath("/html/body/div[2]/div/aside/div[1]/ul[2]/li[2]/text()"))

        # 注册资本
        capital = getXpathValue( html.xpath("/html/body/div[2]/div/aside/div[1]/ul[2]/li[3]/text()"))
        regLocation = getXpathValue( html.xpath("//li[@data-selector='company-address']/text()"))

        # 未融资,100 - 499 人 广州,计算机软件
        company_summary=[ i.strip() for i in  company_summary.split("|")]

        if len(company_summary)!=4:
            clog.error("公司信息总结不是4")
            return

        self.companyFile.write(json.dumps({'company_name': company_name,
                                            'company_status':company_summary[1],
                                           'company_id': company_url,
                                           'industry': company_summary[3],
                                           'regStatus': regStatus,
                                           'estiblishDate': estiblishDate,
                                           'regLocation': regLocation,
                                           'financing':company_summary[0],
                                           'capital':capital,
                                           'site': self.getSite()
                                           }, ensure_ascii=False))
        self.companyFile.write("\n")

    def crawCompany(self):
        # 读取工作,爬取公司信息
        self.companyFile = self.fopen(self.getCompanyPath(), "w", encoding="UTF-8",
                                      auto_mkdir=True)

        jobFile = open(self.getJobPath(), 'r', encoding='UTF-8')

        for job in jobFile:
            obj = json.loads(job)

            self.crawCompanyItem(obj['company_id'])
        self.companyFile.close()
        pass


class quanzhi(Craw):

    def __init__(self):
        Craw.__init__(self)
        self.url='http://www.quanzhi.com/jobs/s-0-6-0-0-0-0-0-0/?kw={keyword}&page={page}#nogo'


        self.headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Fire"}
        # self.jobpath=os.path.join(self.outdir, self.getSite() + "_job.txt")
        # self.companypath = os.path.join(self.outdir, self.getSite() + "_company.txt")

    # def getJobPath(self):
    #     return self.jobpath
    # def getCompanyPath(self):
    #     return self.companypath
    def getSite(self):
        return "quanzhi"

    def crawItem(self,page):

        geturl = self.url.format(keyword=self.getkeyword(), page=page)


        #res=requests.get(geturl   ,   headers=self.headers)
        strw = self.getText(geturl,headers=self.headers)

        if strw==None:
            clog.error("request none at page: {}".format(page))
            return
        self.parseItem(strw,page)



    '''
addnext
addprevious
append
attrib
base
clear
cssselect
extend
find
findall
findtext
get
getchildren
getiterator
getnext
getparent
getprevious
getroottree
index
insert
items
iter
iterancestors
iterchildren
iterdescendants
iterfind
itersiblings
itertext
keys
makeelement
nsmap
prefix
remove
replace
set
sourceline
tag
tail
text
values
xpath
    '''
    def parseItem(self,res,page):

        html = etree.HTML(res)

        # 获取所有li,
        lis=html.xpath("//ul[@class='joblist']/li")

        jobs=[]
        li_xpaths={
            "job_id":"//div[1]/div/a/@href",
            "title":"//div[1]/div/a/text()",
            "salary":"//div[1]/p[1]/span/text()",
            "city":"//div[1]/p[2]/span[1]/text()",
            "work_year":"//div[1]/p[2]/span[2]/text()",
            "edu":"//div[1]/p[2]/span[3]/text()",
            "company":"//div[2]/div/a/text()",
            "company_index":"//div[2]/p[1]/text()",
            "company_status":"//div[2]/p[2]/text()",
            "refresh_date":"//div[1]/div/span[2]/text()",

            "company_id":"//div[2]/div/a/@href"

        }
        # 提取出字段,
        for li in lis:


            # 重新element
            # try:
            # clog.debug( etree.tostring(li).decode().strip())
            li2=etree.HTML( etree.tostring(li))
            # except Exception as e:
            #
            #     clog.error(e.tostring()+"解析li 失败"+str(etree.tostring(li)))
            # job_id=li2.xpath("//div[1]/div/a/@href")
            # title= li2.xpath("//div[1]/div/a/text()")
            # salary=li2.xpath("//div[1]/p[1]/span/text()")
            # city=li2.xpath("//div[1]/p[2]/span[1]/text()")
            # work_year=li2.xpath("//div[1]/p[2]/span[2]/text()")
            # edu = li2.xpath("//div[1]/p[2]/span[3]/text()")
            # company=li2.xpath("//div[2]/div/a/text()")
            # company_id=li2.xpath("//div[2]/div/a/@href")
            # company_index=li2.xpath("//div[2]/p[1]/text()")
            # company_status=li2.xpath("//div[2]/p[2]/text()")
            # refresh_date=li2.xpath("//div[1]/div/span[2]/text()")
            job={}
            for key,value in li_xpaths.items():
                temp = li2.xpath(value)
                if len(temp)!=1:
                    job[key]=''
                else:
                    job[key]=temp[0].strip()


            # print(job_id, title,salary,city,work_year,edu,company,company_id,company_index,company_status,refresh_date)

            print(job)
            job.update({"site":self.getSite()})
            # 解析职位介绍,需要点进去

            job.update({"desc":self.getJobDesc(job['job_id'])})

            self.jobfile.write(json.dumps(job, ensure_ascii=False))
            self.jobfile.write("\n")

        pass
    # 获取职位信息
    def getJobDesc(self,jobid):
        strw = self.getText(jobid)

        if strw==None:
            return
        # 正则表达式查找
        result = re.findall(r'<div class="desc">(.*?)(?<=div)', strw, flags=re.S)
        if len(result)==1:
            result=result[0].replace(" </div",'').strip()
        else:
            result=''
        return result


        pass

    def crawJob(self):
        self.jobfile = self.fopen(self.getJobPath(), "w", encoding="UTF-8",
                                  auto_mkdir=True)
        for i in range(1,100):

            self.crawItem(i)

        self.jobfile.close()
        pass
    #提取company id ,这里company直接是连接
    def crawCompanyItem(self,companyurl):

        clog.info("爬去公司:"+companyurl)

        strw = self.getText(companyurl,headers=self.headers)

        company_id=companyurl
        html = etree.HTML(strw)
        # clog.debug(strw)
        company_name=html.xpath('//input[@id="comname"]/@value')[0]
        company_id=html.xpath('//input[@id="comid"]/@value')[0]

        post_url = 'http://www.quanzhi.com/ajax/company/getComSkyeyeInfo'

        res=requests.post(post_url,data={'comid':company_id},headers=self.getheaders())
        '''result	{…}
skyId	7917140
companyOrgType	有限责任公司(自然人投资或控股)
regStatus	在业
industry	商务服务业
regLocation	北京市海淀区彩和坊路11号6层603室
creditCode	91110108686903609U
estiblishDate	2009年03月27日'''
        print(res.text)
        obj = json.loads(res.text).get('result',None)
        if isinstance(obj,list):
            obj={}

        industry=obj.get("industry",'')
        regStatus=obj.get('regStatus','')
        estiblishDate=obj.get('estiblishDate','')
        regLocation = obj.get('regLocation', '')
        # creditCode=obj.get('creditCode')








        self.companyFile.write(json.dumps({'company_name':company_name,

                                           'company_id':company_id,
                                           'industry':industry,
                                           'regStatus':regStatus,
                                           'estiblishDate':estiblishDate,
                                           'regLocation':regLocation,
                                           'site':self.getSite()
                                           },ensure_ascii=False))
        self.companyFile.write("\n")

        pass
    # 根据工作爬去公司
    def crawCompany(self):
        self.companyFile = self.fopen(self.getCompanyPath(), "w", encoding="UTF-8",
                                  auto_mkdir=True)
        jobFile = open( self.getJobPath(),'r',encoding='UTF-8')

        for job in jobFile:
            obj = json.loads(job)

            self.crawCompanyItem(obj['company_id'])
        self.companyFile.close()

if __name__=='__main__':
    l = liepin()
    l.crawJob()
    #l.crawCompany()
