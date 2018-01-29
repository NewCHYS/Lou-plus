#!/usr/bin/env python3

import sys

def calculator():
	baoxian = 0
	qizhengdian = 3500

	if len(sys.argv) != 2:
		print('Parameter Error')
		return
	try:
		total = int(sys.argv[1])
	except Exception as e:
		print(e)
		return

	if total < 0:
		print('Number less than zero.')
		return

	n1 = total - baoxian - qizhengdian

	if n1 <= 0:
		shuilv = 0
		kouchu = 0
	elif n1 <= 1500:
		shuilv = 0.03
		kouchu = 0
	elif n1 <= 4500:
		shuilv = 0.1
		kouchu = 105
	elif n1 <= 9000:
		shuilv = 0.2
		kouchu = 555
	elif n1 <= 35000:
		shuilv = 0.25
		kouchu = 1005
	elif n1 <= 55000:
		shuilv = 0.3
		kouchu = 2755
	elif n1 <= 80000:
		shuilv = 0.35
		kouchu = 5505
	else:
		shuilv = 0.45
		kouchu = 13505

	yingjiao = n1 * shuilv - kouchu
	print('%.2f' % yingjiao)

if __name__ == '__main__':
	calculator()
