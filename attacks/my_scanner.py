import socket                                                               
import sys                                                                  
from scapy.all import ARP, Ether, srp
import os

'''
target ranges:
    10.12.0.0/24
    10.1.0.0/24
'''
file_name = "scan_results.txt"
# ARP request does not cross a router
#   can only send and receive arp request in the local network
def arp_scan(ip_range):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    answers = srp(packet, timeout=2, retry=1)[0]
    result = []
    for sent, received in answers:
        result.append({'IP': received.psrc, 'MAC': received.hwsrc})

    for res in result:
        print("{:16}    {}".format(res['IP'], res['MAC']))
    return result
                                                                            
def scan_ip(ip, start_port, end_port):                                      
    f = open(file_name, "a")
    ret = tcp_scan(ip, start_port, end_port)                                
    if len(ret) != 0:                                                       
        f.write(ip)
        print(f"IP address {ip} has open ports: ")                          
        for port in ret:                                                    
            f.write(":"+str(port))
            print(f"- {port}")                                              
        f.write("\n")
    f.close()
                                                                            
def scan_range(ip_range, start_port, end_port):                             
    l = ip_range.split('/')                                                 
    free_bits = 32 - int(l[1])                                              
    if free_bits != 8:                                                      
        print("Does not support subnet mask != 24")                         
        exit()                                                              
    begin = l[0][:-1]                                                       
    for i in range(1,50): # Normally 1 to 255 but it takes too long 
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
        except Exception as e:                                              
            print(f"Error scanning port {port}: {e}")                       
    return open_ports                                                       

def main():
    socket.setdefaulttimeout(0.01)                                          
    ips = ["10.12.0.0/24", "10.1.0.0/24" ]
    start = 0                                                               
    end = 100                                                              
    for ip in ips: 
        scan_range(ip,start,end)                                                

                                                                            
if __name__=='__main__':                                                    
    try:
        os.remove("/home/mininet/LINFO2347/scan_results.txt")
    except Exception:
        pass
    main()
    #ip = "192.168.1.0/24"                                                     
    #arp_scan(ip)
