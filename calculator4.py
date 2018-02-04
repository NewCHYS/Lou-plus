#!/usr/bin/env python3

import sys, os, time
from multiprocessing import Process, Queue


class Config():
	def __init__(self, argc):
		self.config = self._read_config(argc)
	
	def _read_config(self, argc):
		config = {}
		try:
			f = open(argc, 'r')
			for x in f:
				if x:
					lines = x.split('=')
					config[lines[0].strip()] = float(lines[1].strip())
			f.close()
		except Exception as e:
			print(e)
			f.close()
			exit()
		return config

	def get_config(self):
		return self.config

class UserData():

	def __init__(self, argd):
		self.userdata = self._read_userdata(argd)

	def _read_userdata(self, argd):
		userdata = {}
		try:
			f = open(argd, 'r')
			for x in f:
				if x != '\n':
					lines = x.split(',')
					userdata[lines[0].strip()] = int(lines[1].strip())
			f.close()
		except Exception as e:
			print(e)
			f.close()
			exit()
		return userdata

	def get_userdata(self):
		return self.userdata


class Args():
	def __init__(self):
		if len(sys.argv) != 7:
			print('Parameter Error')
			exit()
		self.args = sys.argv[1:]

	def get_Args(self):
		arglist = []
		
		for item in ['-c','-d','-o']:
			try:
				index = self.args.index(item)
				arglist.append(self.args[index+1])
			except Exception as e:
				print(e)
		return arglist


class Calaulator():
	
	def __init__(self, baoxian, pid, total):
		self.baoxian = baoxian
		self.pid = pid
		self.total = total

	def get_shuilv(self, yingjiao = 0):
		shuilv_kouchu = ([0, 0], [0.03, 0], [0.1, 105], [0.2, 555], [0.25, 1005], [0.3, 2755], [0.35, 5505], [0.45, 13505])
		list_yingjiao = [0, 1500, 4500, 9000, 35000, 55000, 80000]
		for i,n in enumerate(list_yingjiao):
			if yingjiao > n:
				continue
			else:
				break
		return shuilv_kouchu[i]

	def calculator(self):
		qizhengdian = 3500
		baoxianlv = 0
		for i in ['YangLao', 'YiLiao', 'ShiYe', 'GongShang', 'ShengYu', 'GongJiJin']:
			baoxianlv += self.baoxian[i]
		#print(baoxianlv)
		if self.total < self.baoxian['JiShuL']:
			jishu = self.baoxian['JiShuL']
		elif self.total > self.baoxian['JiShuH']:
			jishu = self.baoxian['JiShuH']
		else:
			jishu = self.total

		baoxianshu = jishu * baoxianlv
		n1 = self.total - baoxianshu - qizhengdian
		n1 = n1 if n1 > 0 else 0
		shuilv, kouchu = self.get_shuilv(n1)
		yingjiao = n1 * shuilv - kouchu
		#print(n1, shuilv, kouchu, yingjiao)
		shuihou = self.total - baoxianshu - yingjiao

		return ('%d,%d,%.2f,%.2f,%.2f' % (int(self.pid), self.total, baoxianshu, yingjiao, shuihou))

	def get_result(self):
		result = self.calculator()
		return result

class Export():
	def __init__(self):
		pass

	def savefile(self, argo, strin):
		try:
			f = open(argo, 'a')
			f.write(strin)			
			f.close()
			#print(strin + " writen OK\n")
		except Exception as e:
			print(e)
			f.close()
			exit()


def read_userdata(argd):
	u = UserData(sys.argv[1:])
	#print(u.get_userdata())
	n = u.get_userdata()
	for i, j in n.items():
		queue_userdata.put(i+':'+j)
	queue_userdata.put('exit')

def calculate(argc):
	c = Config(argd)	
	con = c.get_config()
	print("config: ")
	print(con)
	while true:
		userdata = queue_userdata.get()
		print(userdata)
		if userdata == 'exit':
			queue_savedata.put('exit')
			break
		i, j = userdata.split(':')
		result = Calaulator(con ,i, j).get_result() +'\n'
		queue_savedata.put(result)

def save_data(argo):
	e = Export()
	while true:
		s_data = queue_savedata.get()
		print(s_data)
		if s_data == 'exit':
			break
		print(s_data)
		e.savefile(argo, s_data)


queue_userdata = Queue()
queue_savedata = Queue()
if __name__ == '__main__':
	argd, argc, argo = Args().get_Args()
	p1 = Process(target = read_userdata, args = (argd,))
	p2 = Process(target = calculate, args = (argc,))
	p3 = Process(target = save_data, args = (argo,))
	p1.join()
	p2.join()
	p3.join()
'''		
	#start()
	c = Config(sys.argv[1:])
	#print(c.get_config())
	con = c.get_config()
	u = UserData(sys.argv[1:])
	#print(u.get_userdata())
	n = u.get_userdata()
	res = ''
	for i, j in n.items():
		res = res + Calaulator(con ,i, j).get_result() +'\n'
'''
	
	
