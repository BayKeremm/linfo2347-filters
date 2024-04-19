from ftplib import FTP

def connect_ftp(host, username, password):
    ftp = FTP(host)
    ftp.login(username, password)
    return ftp

def list_files(ftp):
    files = []
    ftp.dir(files.append)
    return files

#def download_file(ftp, filename, local_filename):
#    with open(local_filename, 'wb') as f:
#        ftp.retrbinary('RETR ' + filename, f.write)

def main():
    host = 'ftp.example.com'
    username = 'your_username'
    password = 'your_password'

    # Connect to the FTP server
    ftp = connect_ftp(host, username, password)
    print("Connected to FTP server")

    # List files in the current directory
    files = list_files(ftp)
    print("Files in current directory:")
    for file in files:
        print(file)

    # Download a file
    #filename = 'example.txt'  # Change to the file you want to download
    #local_filename = 'downloaded_file.txt'  # Change to the local filename you want
    #download_file(ftp, filename, local_filename)
    #print(f"Downloaded file '{filename}' as '{local_filename}'")

    # Close the FTP connection
    ftp.quit()
    print("Disconnected from FTP server")

if __name__ == "__main__":
    main()
