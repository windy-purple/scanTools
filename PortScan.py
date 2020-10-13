import time
import socket
from threading import *
import optparse
import subprocess

def Scan(host,port):
	global threadlock
	conn=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		conn.connect((host,port))
#		conn.send(b'version\r\n')
#		results=conn.recv(100)
#		results=results.decode('utf-8')
		threadlock.acquire()
#		time=time.localtime(time.time())
		print('[*] ' +time.strftime('%Y-%m-%d %H:%M:%S')+F' {port}/tcp open '+socket.getservbyport(port, 'tcp'))
#		print(f'[*] {port}/tcp open')
	except:
		pass
#		print('[*]' +time.strftime('%Y-%m-%d %H:%M:%S')+F' {port}/tcp close ')
#		print(f'[+] {port}/tcp close')
	finally:
		threadlock.release()
		conn.close()
	
def main(host):
	print(F'开始扫描主机{host}')
	threads=[]
	for port in range(1,1024):
		t=Thread(target=Scan,args=(host,port))
		threads.append(t)
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	
if __name__=='__main__':
	host=input('请输入主机IP: ')
	start_time=time.time()
	threadlock=Semaphore(value=1)
	main(host)
	end_time=time.time()
	all_time=end_time-start_time
	print('总共耗时: %.2f s'%all_time)