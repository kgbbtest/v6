#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import deal_email_data
import smtplib,email,dkim 
from email.mime.text import MIMEText
from email.header import Header
import dns.resolver 
import random
import re  
import time
import os
import sys#sys.argv
import dnspod
import opendkim
import statistics
import iptable
import random


reload(sys)
sys.setdefaultencoding('utf8')


try:
	sys.argv[1]     #运行别的代码
except Exception:
    print('请输入参数！\n记录and查看进度  python do.py record\n群发邮件  python do.py sendall\n发件统计  python do.py statistics')
    exit()
#deal_email_data.senderemail
#deal_email_data.useremails
#deal_email_data.content_data('subject')
#deal_email_data.content_data('txt')

def mail(useremail,donum,all_num,time_now):
	donum=donum+1
	try:
		message = MIMEText(deal_email_data.rand_words('txt'), 'plain', 'utf-8')
		sender=deal_email_data.senderemail()
		message['From'] =sender  # 发送者
		web=sender.split('@')[1]
		os.system('hostname '+web)
		#sig = dkim.sign(msg, "s1", web, open("/default.private").read()) 
		#msg = sig +
		sig = dkim.sign(message.as_string(), 'default',web, open(os.path.join("/etc/opendkim/keys/"+web+'/', 'default.private')).read())
		message['DKIM-Signature'] = sig[len("DKIM-Signature: "):]
		message['Reply-To']=sender 
		message['from2'] = 'from2'
		message['To'] =useremail
		message['Subject'] = deal_email_data.rand_words('subject')
		message['Date'] =time.strftime("%a, %d %b %Y %H:%M:%S +0800", time.localtime())
		message['Message-ID'] = "<" + str(time.time()) +sender+ ">"
		message['X-Mailer']='webmail client'
		message_str=message.as_string().replace('From: '+sender+'\n','').replace('from2: from2\n','From: '+sender+'\n')
		deal_email_data.sendmail(message['From'],message['To'],message_str)
		message_detail = message['From']+' sendto '+useremail
		left=all_num-donum
		percent=(donum/all_num)*100
		timeuse=time.time()-time_now
	except :
	    print "Error: 无法发送邮件"
	else:
		record_process = str(percent)+'%'+'  deal '+str(donum)+' message  left '+str(left)+'  use '+str(timeuse)+'s  '+message_detail+'\n'
		with open('res/progress.txt','a+') as f:
			f.write(record_process)
		print record_process.replace("\n", "")
def mail_record():
	with open('res/progress.txt','r') as fr:
		record_one= fr.readlines()[-1]
		record_mail = record_one.split('sendto ')[1].replace('"', '').replace("\n", "").replace(' ', '').strip().replace('	', '')
	undomail=open("res/useremail.txt","r").read().split(record_mail)[1]
	with open('res/useremail.txt','w') as f:
		f.write("\n"+undomail)
	print '记录进度成功！'+record_one
def sendemail():
	os.system('rm -rf /var/log/maillog')
	os.system('chmod 777 -R /var/log')
	os.system('service rsyslog restart')
	useremails=deal_email_data.useremails()
	all_num=len(useremails)
	time_now=time.time()
	iptable_reset=0
	for useremail in useremails:
		iptable_reset=iptable_reset+1
		if iptable_reset % 200==0:
			os.system('python do.py iptable ')
		mail(useremail,useremails.index(useremail),all_num,time_now)
		time.sleep(random.randint(12,16))
if sys.argv[1]=='record':	
		mail_record()
elif sys.argv[1]=='sendall':
		sendemail()
elif sys.argv[1]=='dnspod':
	 dnspod.dnspod(sys.argv[2])

elif sys.argv[1]=='opendkim':
     opendkim.opendkim()
elif sys.argv[1]=='statistics':
     statistics.statistics()
elif sys.argv[1]=='iptable':
     iptable.iptable()