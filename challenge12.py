import socket
import sys

def get_args():
    args = sys.argv[1:]
    #print(args)
    try:
        if args[0] == '--host' and args[2] == '--port':
            ip = args[1]
            port = args[3]
        else:
            raise()

        ip_list = ip.split('.')
    #    print(ip_list)
        if len(ip_list) != 4:
            raise()

        for i in ip_list:
            i = int(i)
            if 0 <= i <= 255:
                pass
            else:
                raise()
        port_list = port.split('-')
    #    print(port_list)
        if len(port_list) == 1:
            port = int(port_list[0])
        elif len(port_list) == 2:
            start = int(port_list[0])
            end = int(port_list[1])
            if 0 <= start <= 65535 and 0 <= end <= 65535 and start < end:
                port = range(start, end+1)
            else:
                raise()
        else:
            raise()


    except Exception as e:
        print("Parameter Error")
        print(e)
        sys.exit(1)

    return ip, port

def test_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    n = s.connect_ex((ip,port))
    if n == 0:
        print("{} open".format(port))
    else:
        print("{} closed".format(port))

def scan_ip(ip, port):
    if type(port) == int:
        test_port(ip, port)
    else:
        for i in port:
            test_port(ip, i)


if __name__ == '__main__':
    ip, port = get_args()
    #print(ip)
    #print(port)
    scan_ip(ip, port)

