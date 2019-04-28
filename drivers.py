from work_craws.works import quanzhi
import logging
from craw.fcraw import Craw
from work_craws.works import  WorkCrawFactory
import os
from config.crawconfig import sites

from sync import syncs

# 日志初始化
def initLogger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    simpleFormatter =  logging.Formatter('%(message)s')
    crawLogger = logging.getLogger("craw")
    # 主驱动的日至打印
    driverLogger = logging.getLogger("driver")
    syncLogger = logging.getLogger("sync")

    # 控制台使用简单的格式
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(simpleFormatter)

    fileHandler = logging.FileHandler(filename="/home/gk/PycharmProjects/job_craw/logs/craw.log")
    fileHandler.setFormatter(formatter)
    # 添加handler,有文件和控制台，可以分别设置格式
    crawLogger.addHandler(consoleHandler)
    crawLogger.addHandler(fileHandler)
    driverLogger.addHandler(consoleHandler)
    driverLogger.addHandler(logging.FileHandler(filename="/home/gk/PycharmProjects/job_craw/logs/driver.log"))
    syncLogger.addHandler(consoleHandler)
    syncLogger.addHandler(logging.FileHandler(filename="/home/gk/PycharmProjects/job_craw/logs/sync.log"))
    pass


dlog=logging.getLogger("driver")
def craw_job():


    for key,value in sites.items():
        dlog.info("开始爬取站点:",key)
        c=WorkCrawFactory.getSiteWorker(key)
        c.crawJob()
        dlog.info("爬取{}完成.".format(key))

def craw_company():
    pass
    for key,value in sites.items():
        dlog.info("开始爬取站点:",key)
        c=WorkCrawFactory.getSiteWorker(key)
        c.crawCompany()
        dlog.info("爬取{}完成.".format(key))
# 主菜单类,查询已爬取的和爬取对应的东西




#     主菜单
def usage():
    print('''
    a.数据查询
    0.退出
    1.爬取所有职位
    2.爬去所有公司
    3.同步本地数据到mysql数据库
    4.推送数据到kafka
    
    
    ''')
    what = input("输入代码:")
    if what=="1":
        craw_job()
        usage()
    if what=='2':
        craw_company()
        usage()
    elif what=='0':

        exit(0)
    elif what=='a':
        checkData()
    elif what=='4':
        syncs.push_to_kafka()

def inputkey():
    pass

# 检查数据
def checkData():
    pass
    print("正在收集数据...")
    print("站点列表:")
    print(sites)
    print("----------工作数据-------------")

    rows=["站点\t工作数\t公司数"]
    for key,value in sites.items():
        c=WorkCrawFactory.getSiteWorker(key)

        row=''
        row+=(value+'\t')

        print("工作路径:"+c.getJobPath())
        if  os.path.exists(c.getJobPath()):
            row += (str(len(open(c.getJobPath(),'r').readlines())) + '\t')

        else:
            row+=('没有'+'\t')

        # print("公司路径:" + c.getJobPath())
        if  os.path.exists(c.getCompanyPath()):
            row+=( str(len(open(c.getCompanyPath(), 'r').readlines()))+'\t')
        else:
            row+=('没有'+'\t')
        row+='\n'
        rows.append(row)
    for row in rows:
        print(row+"\n")

    print("-----------------------")
if __name__=="__main__":
    # craw_company()
    initLogger()
    checkData()
    usage()


# qz= quanzhi()
# qz.craw()



