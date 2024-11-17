import os
import time
from stem.control import Signal 
from stem.control import Controller
import sys
from requests import get
import subprocess

banner = '''
██╗██████╗        ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
██║██╔══██╗      ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
██║██████╔╝█████╗██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
██║██╔═══╝ ╚════╝██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
██║██║           ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
╚═╝╚═╝            ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                            '''
YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
GREEN = '\033[32;1m'
RED = '\033[31;1m'
WHITE = '\033[m'

print('--'*15 + 'WELL-COME-TO' + '--'*15)
print(banner)
print('created by : 14M5K1D')
print('--'*40)

class ChangeIp:

    def __init__(self,passwd="Torpassword@123",change=50,intervals=60):
        self.password=passwd
        self.intervals=intervals
        self.change=change


    def check_pkg(self):
        if os.system('which tor > /dev/null ') != 0:
            sys.exit('[*] tor is not installed..! , install it by "sudo apt-get install tor" ')
        else:
            pass

    # def open_firefox(self):

    
    def __get_hash_password(self):
        command = ['tor', '--hash-password', self.password ]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.stdout:
                return result.stdout.strip().split()[-1]
            
            if result.error:
                sys.exit(f"[!]{RED}{e}")

        except Exception as e:
            sys.exit(f"{RED} Failed to generated hash password due to error : {e}")
            

    def _configure_torrc(self):
        
        print(f'{WHITE}[*] Configuring the torrc file....!')
        torrc_file_path = "/etc/tor/torrc"
        hash_password = self.__get_hash_password()
        try:
            with open(torrc_file_path, 'r') as fl:
                lines = fl.readlines()

            for i in range(len(lines)):
                if "ControlPort 9051" in lines[i]:
                    lines[i] = "ControlPort 9051"
                
                if "HashedControlPassword" in lines[i]:
                    lines[i] = f"HashedControlPassword {hash_password}"

            with open(torrc_file_path, 'w') as file:
                file.writelines(lines)

            print(f'{GREEN}[*] Torrc file is configured succesfully')
        except Exception as e:
            print(e)


    def show_ip(self):
        proxies={
                'http':'socks5://127.0.0.1:9050',
                'https':'socks5://127.0.0.1:9050'
                }
        try:
            ip=get('https://api.ipify.org',proxies=proxies)

        except Exception as err:
            print(str(err))
            sys.exit()
        else:
            return ip.text



    def _check_root(self):
        if os.getuid()!=0:
            sys.exit('This script must be run as root..!')
        else:
            self.check_internet()


    def check_internet(self):
        print('[*] checking for internet connetcion....!')
        time.sleep(2)
        if not os.system('ping -c 2 google.com > /dev/null '):
            print(f'{GREEN}[*] CONNECTED')
            self.start_tor()
        else:
            sys.exit('[*] Connection failed...! Please check your internet..!')


    def start_tor(self):
        self.check_pkg()
        self._configure_torrc()

        try:
            if not os.system('service tor start'):
                time.sleep(1)
                print('[*] CONNECTED TO TOR')
                self._renew_ip()
        except Exception as e:
            print('Oops ..!,Something went wrong')
            print(str(e))
            os.system('service tor stop')
            sys.exit()
        except KeyboardInterrupt:
            os.system('service tor stop')

    def _renew_ip(self):
        print(WHITE)
        try: 
            for i in range(0,self.change-1):
                print('your ip adress is : ',self.show_ip())
                time.sleep(self.intervals)
                with Controller.from_port(port = 9051) as controller:
                    controller.authenticate(password=self.password)
                    controller.signal(Signal.NEWNYM)
            print('Terminating script.....')
            time.sleep(2)
            os.system('service tor stop')
            sys.exit()

        except Exception as error:
            print(str(error))
            os.system('service tor stop')
            sys.exit(f'[!]{RED}unable to connected to port 9051')

    def start_ip_changer(self):
        self._check_root()

obj = ChangeIp(change=10,intervals=20)
obj.start_ip_changer()

# interval = '20 seconds'
# password = None
# change = '0 times'

# def main():
#     def setcmd(option, value):
#         global interval, password, change
#         if option.lower() == 'interval':
#             if not value.isdigit():
#                 print(f'{RED}[!] ERROR: {WHITE}Please enter a number.')
#             else:
#                 if not int(value)>=20:
#                     print(f'[!] ERROR: {WHITE}Please enter a number which is greater than or equal to 20.')
#                 else:
#                     interval = f'{value} seconds'
#                     print(f'{GREEN} {option} ==> {value} seconds {WHITE}')
#         elif option.lower() == 'password':
#             password = value
#             print(f'{GREEN} {option} ==> {value} {WHITE}')
#         elif option.lower() == 'times_to_change':
#             if not value.isdigit():
#                 print(f'{RED}[!] ERROR: {WHITE}Please enter a number.')
#             else:
#                 if int(value) > 200:
#                     print(f'{RED}[!] ERROR: {WHITE}You can only change IP for 200 times max.')
#                 else:
#                     change = f'{value} times'
#                     print(f'{GREEN} {option} ==> {value} times {WHITE}')
#         else:
#             print(f'{RED}ERROR: INVALID OPTION SELECTED.{WHITE}')
#     while True:
#         x = input(f'{WHITE}[{RED}IP-CHANGER{WHITE}] : ')
#         if 'set' in x.lower() and len(x.split(' ')) > 1:
#             setcmd(x.split(' ')[1],x.split(' ')[2])
#         elif 'options' in x.lower():
#             print('----OPTIONS----\t----VALUE----\t----DESCRIPTION----')
#             print(f'interval\t{interval}\tinterval between changes (in seconds).')
#             print(f'password\t{password}\tthe password to authenticate with tor(the passsword you used to create the hashed password)')
#             print(f'times_to_change\t{change}\tnumber of times you want to change your ip (max is 200)\n')
#         elif 'help' in x.lower():
#             print('---COMMANDS--\t---INFO---')
#             print('set\tset a option {set <option name> <value>')
#             print('run\trun the ip changer with the available options.')
#             print('options\tshow available options and their current values.')
#             print('help]tshow this help message')
#             print('exit\texit the script.')
#         elif 'run' in x.lower():
#             if password != None and change != '0 times':
#                 print(f'proceeding with the options:-\ninterval = {interval}\npassword = {password}\ntimes_to_change = {change}\n')
#                 try:
#                     run = changeip(password,int(change.split(' ')[0]),int(interval.split(' ')[0]))
#                     run._check_root()
#                 except Exception as e:
#                     print(f'{RED} Some Error Occoured:- %s\n Exitting script...'%(e.args))
#                     os.system('service tor stop')
#                     exit()
#             else:
#                 print(f'{RED}ERROR: {WHITE}Some of the options are not set.')
#         elif 'exit' in x.lower():
#             exit()
#         else:
#             print(f'{RED}ERROR: {WHITE} Invalid Command.')
# main()
