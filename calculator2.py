#!/usr/bin/env python3

import sys


def get_shuilv(yingjiao = 0):
	shuilv_kouchu = ([0, 0], [0.03, 0], [0.1, 105], [0.2, 555], [0.25, 1005], [0.3, 2755], [0.35, 5505], [0.45, 13505])
	list_yingjiao = [0, 1500, 4500, 9000, 35000, 55000, 80000]
	i = 0
	for n in list_yingjiao:
		if yingjiao > n:
			i += 1
		else:
			break
	return shuilv_kouchu[i]

def yanzheng():
	total = []
	if len(sys.argv) < 2:
		print('Parameter Error')
		exit()
	for arg in sys.argv[1:]:
		people = arg.split(':')
		try:
			id1 = int(people[0])
			total1 = int(people[1])
			if id1 < 0 or total1 < 0:
				raise()
		except Exception as e:
			print('Parameter Error')
			exit()
		total.append((id1, total1))
	return total
'''
	if total < 0:
		print('Number less than zero.')
		exit()
'''


def calculator(pid = 0, total = 0):
	baoxian = {'yanglao':0.08, 'yiliao':0.02, 'shiye':0.005, 'gongshang':0, 'shengyu':0, 'gongjijin':0.06}
	qizhengdian = 3500
	baoxianlv = 0
	for i, j in baoxian.items():
		baoxianlv += j
	#print(baoxianlv)
	
	baoxianshu = total * baoxianlv
	n1 = total - baoxianshu - qizhengdian
	shuilv, kouchu = get_shuilv(n1)
	yingjiao = n1 * shuilv - kouchu
	shuihou = total - baoxianshu - yingjiao

	print('%d:%.2f' % (pid, shuihou))


def start():
	allpeople = yanzheng()
	for i in allpeople:
		calculator(i[0], i[1])
	return
if __name__ == '__main__':
	start()
