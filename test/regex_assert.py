# 正则表达式零宽断言测试
import re
'''
职位详情
CDG企业发展事业群/支付基础平台与金融应用线/平台研发部
18428-财付通清算业务测试工程师（深圳）
岗位要求：
"3年及其以上测试工作经验；
熟悉Unix/Linux工作环境，至少掌握一门常用脚本语言(如shell,perl,python等)；
熟练掌握常用数据库操作，最好有mysql经验；
熟悉一门高级编程语言，要求至少可以参加代码检视，有C/C++经验优先，有性能测试经验者优先；
了解自动化测试思想，有自动化测试经验者优先；
有互联网软件工作经验，了解互联网行业，有金融、证券或支付系统测试经验者优先。"
岗位职责：
"负责财付通基础支付（清算）业务及相关业务产品的集成、系统测试工作；
参与项目开发全流程。"
 
查找出上面的职位详情的内容

'''

with open("regex_assert.html",'r',encoding='UTF-8') as f:
    strw = f.read()
    # print(strw)

    regex = ""
    # 断言后面是</div>结束的(?<=div) (.*?)是非贪婪的,贪婪的话中间可能会有很多个div
    result=re.findall('<div class="content content-word">(.*?)(?<=div)',strw,flags=re.S)[0]
    print(result.replace(" </div",'').strip())