# 在这里将master  broker作为生产者，slave节点启动console消费者消费
# 1.只有一个消费者
# 2.slave1，和slave2分别在不懂的消费的group里面
'''
1.现在集群启动zookeeper和kafka 服务
kafka-server-start.sh config/server.properties &

2.修改
host    brokerid
master  0
slave1  1
slave2  2

3.在master上启动生产者
消息主题为kafka_python_test


启动kafka消费者，在终端里测试，在slave1里执行


'''
from kafka import KafkaProducer

topic='kafka_python_test'
#9092为kafka 配置文件server.properties里的listeners的配置
# 在master上启动消费者
producer = KafkaProducer(bootstrap_servers=['192.168.3.100:9092'])

for i in range(1,3):
    # 发送消息，value必须是bytes类型,发送后，可以查看topic,send参数是bytes类型的
    # 使用kafka-topic.sh --list --zookeeper master:2181,slave1:2181,slave2:2181 命令

    producer.send(topic,b'FormatFa')
# 要调用close才能成功发送
producer.close()
