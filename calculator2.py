#!/usr/bin/env python3

import sys


def get_shuilv(yingjiao):
	shuilv_kouchu = ([0, 0], [0.03, 0], [0.1, 105], [0.2, 555], [0.25, 1005], [0.3, 2755], [0.35, 5505], [0.45, 13505])
	list_yingjiao = [0, 1500, 4500, 9000, 35000, 55000, 80000]
	i = 0
	for n in list_yingjiao:
		if yingjiao > n:
			i += 1
		else:
			break
	return shuilv_kouchu[i]

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

	shuilv, kouchu = get_shuilv(n1)

	yingjiao = n1 * shuilv - kouchu
	print('%.2f' % yingjiao)

if __name__ == '__main__':
	calculator()
