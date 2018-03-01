# -*- coding: utf-8 -*-

import re 
from datetime import datetime


def open_parser(filename):
    with open(filename) as logfile:
        pattern = (r''
                   '(\d+.\d+.\d+.\d+)\s-\s-\s'  
                   '\[(.+)\]\s'  
                   '"GET\s(.+)\s\w+/.+"\s' 
                   '(\d+)\s'  
                   '(\d+)\s'  
                   '"(.+)"\s'  
                   '"(.+)"'  
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():
    logs = open_parser('/home/shiyanlou/Code/nginx.log')
    #print(logs)
    ip_dict = {}
    url_dict = {}
    ip_temp = {}
    url_temp = {}
    value_temp = 0
    key_temp = ''
    for i in logs:
        if '11/Jan/2017' in i[1]:
            ip_temp[i[0]] = ip_temp.get(i[0], 0) + 1
        if i[3] == '404':
            url_temp[i[2]] = url_temp.get(i[2], 0) + 1

    for k, v in ip_temp.items():
        if v > value_temp:
            value_temp = v
            key_temp = k
    ip_dict[key_temp] = value_temp

    value_temp = 0

    for k, v in url_temp.items():
        if v > value_temp:
            value_temp = v
            key_temp = k
    url_dict[key_temp] = value_temp    

    return ip_dict, url_dict


if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)

