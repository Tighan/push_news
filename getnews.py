import httplib2,time,sqlite3
from bs4 import BeautifulSoup
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
from gettime import printtime 
#-----------------------------
header={"User-Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER"}
url='http://110.85.164.243:4505/otype.asp?classid=1'

#-----------------------------
cx=sqlite3.connect('/root/push_news/data.db')
cu=cx.cursor()
h=httplib2.Http()
#cx.execute('create table gs(id,title)')
#cx.execute('insert into gs values(0,null)')
#-----------------------------
def get_title_from_web(url):#获取当前网站标题
	resp,cont=h.request(url)
	soup=BeautifulSoup(cont,'html.parser')
	soupe=soup.find_all('a')
	return soupe[16].string#title
def get_title_from_database():#获取当前数据库标题
	cu.execute('select title from gs')
	title=cu.fetchall()[0]
	return title
def update_title(title):#更新标题至数据库
	cu.execute("update gs set title='%s' where id = 0"%title)
	cx.commit()
def send_message(title):
	sender='421346755@qq.com'
	receiver='2575545003@qq.com'
	subject='更新公告-->'+title
	smtpserver='smtp.qq.com'
	username='421346755@qq.com'
	password='han19940706'
	text="你关注的公告有更新辣o(≧v≦)o~~!!"+'\n'+'本次更新公告标题为：'+title
	msg=MIMEText(text,'plain','utf-8')
	msg['Subject'] = Header(subject,'utf-8')
	smtp = smtplib.SMTP()  
	smtp.connect(smtpserver)  
	smtp.login(username, password)  
	smtp.sendmail(sender, receiver, msg.as_string())  
	smtp.quit()  

title_now=get_title_from_web(url)
title_data=get_title_from_database()
if title_now!=title_data[0]:
    update_title(title_now)
    send_message(title_now)
print('update at'),printtime() 
