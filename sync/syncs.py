from craw.fcraw import Craw
from work_craws.works import WorkCrawFactory
from config.crawconfig import sites
import logging

# kafka生产者，
from kafka import KafkaProducer


log = logging.getLogger("sync")
log.setLevel(logging.DEBUG)
# 推送数据到mysql
def push_to_mysql(craw):
    pass

#推送数据到kafka,读取数据,
'''
1.有两个topic,分别是job,company

2.在master上启动生产者
将数据一行一行的以json的格式发送过去


'''
def push_to_kafka():

    #读取爬取到的各个站点的数据
    producer = KafkaProducer(bootstrap_servers=['192.168.3.100:9092'])

    # 爬取的工作和公司的主题
    topic_job='craw_job'
    topic_company='craw_company'

    # 循环所有站点的数据
    for key,value in sites.items():
        print("读取站点:",key)

        craw = WorkCrawFactory.getSiteWorker(key)
        print(craw)
    #     读取job company
        #发送job到kafka消息队列
        log.info("工作数据目录:"+craw.getJobPath())
        print(craw.getJobPath())
        for job in open(craw.getJobPath(),'r',encoding='UTF-8'):
            log.info("send :"+job)
            producer.send(topic_job,job.encode())

        for company in open(craw.getCompanyPath(),'r',encoding='UTF-8'):
            producer.send(topic_company,company.encode())




