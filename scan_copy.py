import requests
from threading import *
import os
import re
import time
import sys
from optparse import OptionParser
import queue

global timeout1
global thread_count


def product_queue(q,filename):
	f = open(filename,'r')
	for line in f.readlines():
		line = line.strip()
		q.put(line)
	f.close()

def scan(q):
	global timeout1
	headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
	while True:
		try:
			if not q.empty():
				url = q.get()
				r = requests.get(url,headers = headers,timeout = timeout1)
				if r.status_code == 200:
					print(f'[*] {url} 200')
				else:
					print(f'[+] {url} {r.status_code}')
			else:
				break
		except:
			print(f'[-] {url}  timeout')
	
def check_parameters():
	global timeout1
	global thread_count
	flag = os.path.isfile('setting.txt')
	if flag == True:
		with open('setting.txt','r') as f:
			for line in f.readlines():
				line.strip()
				list = line.split()
				if list[0] == 'timeout':
					timeout1 = int(list[1])
				if list[0] == 'thread_count':
					thread_count = list[1]
	else:
		f = open('setting.txt','a')
		f.write('timeout 3\nthread_count 20\n')
		timeout1 = 3
		thread_count = 20
		f.close()
		
def birth(flag,host):
	list = ['txt','rar','zip','xls','pdf']
	list1 = host.split('.')
	x = list1[0]+list1[1]+list1[2]
	filename = x + '.txt'
	f = open(filename,'a+')
	list2 = [host,list1[1],list1[1].upper(),list1[1].lower(),list1[1].capitalize(),x,x.upper(),x.lower(),x.capitalize()]
	for i in list:
		for k in list2:
			data = 'http://' + host + '/' + k + '.' + i
			f.write(data)
			f.write("\n")
	f.close()
	fo = open(filename,'a+')
	filename1 = 'PHP.txt'
	filename2 = 'ASP.txt'
	filename3 = 'JSP.txt'
	if flag == 1:
		fo1 = open(filename1,'r')
		for line in fo1.readlines():
			line = line.strip()
			line = 'http://' + host + line
			fo.write(line)
			fo.write('\n')
		fo1.close()
	if flag == 2:
		fo2 = open(filename2,'r')
		for line in fo2.readlines():
			line = line.strip()
			line = 'http://'+ host + line
			fo.write(line)
			fo.write('\n')
		fo2.close()
	if flag == 3:
		fo3 = open(filename3,'r')
		for line in fo3.readlines():
			line = line.strip()
			line = 'http://' + host + line
			fo.write(line)
			fo.write('\n')
		fo3.close()
	if flag == 4:
		fo4 = open(filename1,'r')
		for line in fo4.readlines():
			line = line.strip()
			line = 'http://' + host + line
			fo.write(line)
			fo.write('\n')
		fo4.close()
		fo5 = open(filename2,'r')
		for line in fo5.readlines():
			line = line.strip()
			line = 'http://' + host + line
			fo.write(line)
			fo.write('\n')
		fo5.close()
		fo6 = open(filename3,'r')
		for line in fo6.readlines():
			line = line.strip()
			line = 'http://' + host + line
			fo.write(line)
			fo.write('\n')
		fo6.close()
	fo.close()
	return filename
	
def check_host(host):
	pattern = re.match(r'\w+.\w+.\w+',host)
	if pattern == None:
		flag = 0
	else:
		flag = 1
	return flag
	
def check(host):
	list = ['php','asp','jsp']
	flag = 0
	for i in list:
		url = 'http://' + host + '/index.' + i
		headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
		r = requests.get(url,headers = headers)
		if r.status_code == 200:
			if i == 'php':
				flag = 1
			if i == 'asp':
				flag = 2
			if i == 'jsp':
				flag = 3
			break
	if flag == 0:
		flag = 4
	return flag
	
def start_scan(q):
	global thread_count
	threads = []
	for i in range(int(thread_count)):
		t = Thread(target = scan,args = (q,))
		t.start()
		threads.append(t)
	return threads
	
def main():
	global timeout1
	global thread_count
	host = input('请输入站点网址:')
	flag3 = check_host(host)
	if flag3 == 0:
		print('输入有错误!')
		sys.exit(0)
	else:
		check_parameters()
		print(f'开始检查站点类型\t{time.localtime(time.time()).tm_year}-{time.localtime(time.time()).tm_mon}-{time.localtime(time.time()).tm_mday}:{time.localtime(time.time()).tm_hour}:{time.localtime(time.time()).tm_min}:{time.localtime(time.time()).tm_sec}')
		flag1 = check(host)
		if flag1 == 1:
			print('站点类型:php')
		if flag1 == 2:
			print('站点类型:asp')
		if flag1 == 3:
			print('站点类型:jsp')
		if flag1 == 4:
			print('站点类型:无法识别  是否继续:y/n?')
			flag2 = input()
			if flag2 == 'n' or flag2 == 'N' or flag2 == 'no':
				sys.exit(0)
			else:
				pass
		print("开始生成扫描字典")
		filename = birth(flag1,host)
		print(f'扫描字典生成完毕\t{time.localtime(time.time()).tm_year}-{time.localtime(time.time()).tm_mon}-{time.localtime(time.time()).tm_mday}:{time.localtime(time.time()).tm_hour}:{time.localtime(time.time()).tm_min}:{time.localtime(time.time()).tm_sec}')
		print('开始扫描:')
		start_time = time.time()
		q = queue.Queue()
		t = Thread(target = product_queue,args = (q,filename))
		t.start()
		threads = []
		threads = start_scan(q)
		for t in threads:
			t.join()
		end_time = time.time()
		time1 = end_time - start_time
		print(f'总共耗时:{time1} s')
	
if __name__ == '__main__':
	main()
	
		