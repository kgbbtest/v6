import sys#sys.argv
import os
import random 


def iptable():
	os.system('iptables -t nat -F POSTROUTING')
	ip = open("res/ip.txt","r").read().split('\n')
	web = open("res/web.txt","r").read().split('\n')
	ip_list=ip
	ip_list_num=len(ip_list)

	random.shuffle(ip_list)
	for ip in ip_list:
		num=ip_list.index(ip)
		os.system('ip6tables  -t nat -I POSTROUTING -m state --state NEW -p tcp --dport 25 -o em1 -m statistic --mode nth --every '+str(ip_list_num)+' --packet '+str(num)+'  -j SNAT --to-source   ' + ip)
