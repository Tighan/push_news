import httplib2,time
import xml.etree.ElementTree as ET
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header 
import sqlite3
cx=sqlite3.connect('/root/push_news/kjdb.db')
cu=cx.cursor()
#cx.execute('create table kaijiang(id,text)')
#cx.execute('insert into kaijiang values(0,null)')
header={"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER"}
http=httplib2.Http()
url='http://www.77190.com:98/wz/scores1.xml'
init=''
animals=['鼠','牛','虎','兔','龙','蛇','马','羊','猴','鸡','狗','猪']
key=[8,7,6,5,4,3,2,1,12,11,10,9]
dic=dict(zip(key,animals))
red=[1,2,7,8,12,13,18,19,23,24,29,30,34,35,40,45,46]
blue=[3,4,9,10,14,15,20,25,26,31,36,37,41,42,47,48]
green=[5,6,11,16,17,21,22,27,28,32,33,38,39,43,44,49] 
def update_text(text):#更新标题至数据库
    cu.execute("update kaijiang set text='%s' where id = 0"%text)
    cx.commit()
def get_text_from_database():#获取当前数据库标题
    cu.execute('select text from kaijiang')
    text=cu.fetchall()[0]
    return text
def return_animal(num):
    while num>12:
        num=num-12
    bo=''
    if num in red:
        bo='红波'
    elif num in blue:
        bp='蓝波'
    else:
        bo='绿波'
    return (dic[num],bo)
def send_message(QS,T,SX,YS):
    sender='421346755@qq.com'
    receiver='2575545003@qq.com'
    subject='开奖公告-->第'+QS+'期'
    smtpserver='smtp.qq.com'
    username='421346755@qq.com'
    password='han19940706'
    text="开奖了╭(￣m￣*)╮，好紧张！"+'\n'+'期数:'+QS+'\n'+'特码:'+T+'\n'+'生肖:'+SX+'\n'+'颜色:'+YS
    msg=MIMEText(text,'plain','utf-8')
    msg['Subject'] = Header(subject,'utf-8')
    smtp = smtplib.SMTP()  
    smtp.connect(smtpserver)  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, msg.as_string())  
    smtp.quit()  
while True:
    time.sleep(1)
    resp,cont=http.request(url)
    strd=cont.decode('gb2312').encode('utf-8').decode('utf-8')
    str=strd.replace('gb2312','utf-8')
    root=ET.fromstring(str)
    result=root[0][0].text#开奖结果，格式为：期数，平码 平码 平码 平码 平码 平码 T 特码
    if 'T' in result:
        text_data = get_text_from_database()[0]
        if text_data != result:
            Q=result[0:3]
            TM=int(result[-2:])
            send_message(Q,result[-2:],return_animal(TM)[0],return_animal(TM)[1])
            update_text(result)
            break
        break
