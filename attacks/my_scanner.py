import socket
import sys


def scan_ip(ip, start_port, end_port):
    ret = tcp_scan(ip, start_port, end_port)
    if len(ret) != 0:
        print(f"IP address {ip} has open ports: ")
        for port in ret:
            print(f"- {port}")

def scan_range(ip_range, start_port, end_port):
    l = ip_range.split('/')
    free_bits = 32 - int(l[1])
    if free_bits != 8:
        print("Does not support subnet mask != 24")
        exit()
    begin = l[0][:-1]
    for i in range(1,255):
        ip = begin + str(i)
        scan_ip(ip, start_port, end_port)
    


def tcp_scan(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port,end_port+1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            result = sock.connect_ex((ip, port))

            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            print(f"Error scanning port {port}: {e}")
    return open_ports


if __name__=='__main__':
    socket.setdefaulttimeout(0.01)
    ip = "192.168.1.1"
    start = 0
    end = 80
    scan_ip(ip,start,end)