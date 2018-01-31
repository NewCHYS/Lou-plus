#!/usr/bin/env python3

import sys, os

class Config():
	def __init__(self, arglist):
		self.config = self._read_config(arglist)
	
	def _read_config(self, arglist):
		config = {}
		try:
			f = open(arglist[arglist.index('-c')+1], 'r')
			for x in f:
				if x != '\n':
					lines = x.split('=')
					config[lines[0].strip()] = float(lines[1].strip())
				#print(config)
			f.close()
		except Exception as e:
			print(e)
			f.close()
			exit()
		return config

	def get_config(self):
		return self.config

class UserData():

	def __init__(self, arglist):
		self.userdata = self._read_userdata(arglist)

	def _read_userdata(self, arglist):
		userdata = {}
		try:
			f = open(arglist[arglist.index('-d')+1], 'r')
			for x in f:
				if x != '\n':
					lines = x.split(',')
					userdata[lines[0].strip()] = int(lines[1].strip())
				#print(config)
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
		arglist = {}
		
		for item in ['-c','-d','-o']:
			try:
				index = self.args.index(item)
				total[index] = self.args[index+1]
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

	def savefile(self, arglist, strin):
		try:
			f = open(arglist[arglist.index('-o')+1], 'w')
			f.write(strin)			
			f.close()
			#print(strin + " writen OK\n")
		except Exception as e:
			print(e)
			f.close()
			exit()


if __name__ == '__main__':
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
	e = Export()
	e.savefile(sys.argv[1:], res)
	