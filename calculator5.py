#!/usr/bin/env python3

import sys, os, time
from multiprocessing import Process, Queue
from datetime import datetime
import configparser
import getopt


class Config():
	def __init__(self, argCity, argc):
		self.argc = argc
		self.city = argCity
	
	def _read_config(self):
		config = {}
		try:
			c = configparser.ConfigParser()
			c.read(self.argc, encoding='utf-8')
			ret = c.items(self.city.upper())
		except Exception as e:
			#print('Config Error')
			print(e)
			#print('in Config')
			f.close()
			exit()
		for i in ret:
			config[i[0].upper()] = float(i[1])
		return config

	def get_config(self):
		return self._read_config()

class UserData():

	def __init__(self, argd):
		self.argd = argd

	def get_userdata(self):
		x = True
		try:
			f = open(self.argd, 'r')
			x = f.readline()
			while x:				
				lines = x.split(',')
				yield lines[0].strip(), int(lines[1].strip())
				x = f.readline()
				#print(userdata)
			f.close()
		except Exception as e:
			#print('UserData Error')
			print(e)
			#print('in Userdata')
			f.close()
			exit()
		return


class Calaulator():	
	def __init__(self, baoxian, pid, total):
		self.baoxian = baoxian
		self.pid = pid
		self.total = total

	def get_shuilv(self, yingjiao = 0):
		shuilv = ([-1, 0.03, 0], [1500, 0.1, 105], [4500, 0.2, 555], [9000, 0.25, 1005], [35000, 0.3, 2755], [55000, 0.35, 5505], [80000, 0.45, 13505])
		for i,n in enumerate(shuilv):
			if yingjiao > n[0]:
				continue
			else:
				break
		return shuilv[i-1][1], shuilv[i-1][2]

	def calculator(self):
		qizhengdian = 3500
		baoxianlv = 0
		for i in ['YangLao', 'YiLiao', 'ShiYe', 'GongShang', 'ShengYu', 'GongJiJin']:
			baoxianlv += self.baoxian[i.upper()]
		#print(baoxianlv)
		if self.total < self.baoxian['JiShuL'.upper()]:
			jishu = self.baoxian['JiShuL'.upper()]
		elif self.total > self.baoxian['JiShuH'.upper()]:
			jishu = self.baoxian['JiShuH'.upper()]
		else:
			jishu = self.total

		baoxianshu = jishu * baoxianlv
		n1 = self.total - baoxianshu - qizhengdian
		n1 = n1 if n1 > 0 else 0
		shuilv, kouchu = self.get_shuilv(n1)
		yingjiao = n1 * shuilv - kouchu
#		print(n1, shuilv, kouchu, sep=' ')
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
			#print('in Export')
			f.close()
			exit()


def read_userdata(argd):
	u = UserData(argd)
	n = u.get_userdata()
	#print('Userdata')
	#print(n)
	for i, j in n:
		queue_userdata.put(str(i) + ':' + str(j))
	#print('p1 exit')
	queue_userdata.put('exit')

def calculate(argCity, argc):
	con = Config(argCity, argc).get_config()
	while True:
		userdata = queue_userdata.get()
		#print(userdata)
		if userdata == 'exit':
			#print('p2 exit')
			queue_savedata.put('exit')
			break
		i, j = userdata.split(':')
		result = Calaulator(con ,int(i), int(j)).get_result()
		time_now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		result += ',' + time_now
		queue_savedata.put(result)

def save_data(argo):
	e = Export()
	while True:
		s_data = queue_savedata.get()
		#print(s_data)
		if s_data == 'exit':
			break
		#print(s_data)
		e.savefile(argo, s_data)


def get_args():
	opts = {}
	try:
		opt, args = getopt.getopt(sys.argv[1:], "hc:d:o:C:", ["help"])
	except:
		print('ParamError.')
		print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
		sys,exit(-1)

	for k, y in opt:
		if k in ('-h', '--help'):
			print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
			sys.exit(0)
		opts[k] = y
	if opts.get('-c') and opts.get('-d') and opts.get('-o'):
		return opts
	else:
		print('ParamError.')
		print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
		sys,exit(-1)

queue_userdata = Queue()
queue_savedata = Queue()
if __name__ == '__main__':
	args = get_args()
	#print(argc, argd, argp, sep = '\n')
	p1 = Process(target = read_userdata, args = (args['-d'],))
	p2 = Process(target = calculate, args = (args.get('-C', 'default'), args['-c']))
	p3 = Process(target = save_data, args = (args['-o'],))
	p1.start()
	p2.start()
	p3.start()
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
	
	
