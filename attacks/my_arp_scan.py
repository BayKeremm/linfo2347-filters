import socket
import sys
from scapy.all import ARP, Ether, srp
import os

'''
target ranges:
    10.12.0.0/24
    10.1.0.0/24
'''

def arp_scan(ip):
    f = open("arp_res.txt", "a")
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    answers = srp(packet, timeout=2, retry=1, verbose=False)[0]
    result = []
    for sent, received in answers:
        result.append({'IP': received.psrc, 'MAC': received.hwsrc})
        f.write(ip)
        f.write(" ")
        f.write(received.hwsrc)
        f.write("\n")
    if(len(result) > 0):
        print(f"IP address {ip} has the following MAC addresses: ")
        for res in result:
            print(f"- {res['MAC']}")
    f.close()
    return result

def scan_range(ip_range, start_port, end_port):
    l = ip_range.split('/')
    free_bits = 32 - int(l[1])
    if free_bits != 8:
        print("Does not support subnet mask != 24")
        exit()
    begin = l[0][:-1]
    for i in range(1,50): # Normally 1 to 255 but it takes too long
        ip = begin + str(i)
        arp_scan(ip)

def main():
    socket.setdefaulttimeout(0.01)
    ips = ["10.12.0.0/24", "10.1.0.0/24" ]
    start = 0
    end = 100
    for ip in ips:
        scan_range(ip,start,end)


if __name__=='__main__':
    try:
        os.remove("/home/mininet/LINFO2347/arp_res.txt")
    except Exception:
        pass
    main()
