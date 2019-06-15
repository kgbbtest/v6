#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys#sys.argv
import os 


def opendkim():
	web = open("res/web.txt","r").read().split('\n')
	os.system('echo '' > /etc/opendkim/KeyTable')
	os.system('echo '' > /etc/opendkim/SigningTable')
	os.system('echo localhost > /etc/opendkim/TrustedHosts')
	os.system("mkdir  /etc/opendkim/keys")
	for w in web :
			w=w.replace('"', '').replace("\n", "").replace(' ', '').strip().replace('	', '')
			os.system("mkdir  /etc/opendkim/keys/"+w)
			os.system('opendkim-genkey --domain='+w+'  --directory=/etc/opendkim/keys/'+w+'/')
			os.system('echo "default._domainkey.'+w+' '+w+':default:/etc/opendkim/keys/'+w+'/default.private" >> /etc/opendkim/KeyTable')
			os.system('echo "*@'+w+' default._domainkey.'+w+'" >> /etc/opendkim/SigningTable')
			os.system('echo "'+w+'" >> /etc/opendkim/TrustedHosts')
			print(w+'创建密匙成功！')

	os.system('chown opendkim:opendkim -R /etc/opendkim/')
	os.system('chmod -R 700 /etc/opendkim')
	os.system('systemctl restart opendkim.service')
	os.system('systemctl restart postfix.service')


