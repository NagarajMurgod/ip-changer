import os
import time
from stem.control import Signal 
from stem.control import Controller
import sys
from requests import get

print('--'*12 + 'WELL-COME-TO' + '--'*12)
os.system("figlet IP - Changer ")
print('created by : 14M5K1D')
print('--'*30)

class changeip:

    def __init__(self,passwd,change,intervals):
        self.password=passwd
        self.intervals=intervals
        self.change=change


    def check_pkg(self):
        if os.system('which tor > /dev/null ')!=0:
            sys.exit('[*] tor is not installed..! , install it by "sudo apt-get install tor" ')
        else:
            pass


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
            print('[*] CONNECTED')
            self.start_tor()
        else:
            sys.exit('[*] Connection failed...! Please check your internet..!')


    def start_tor(self):
        self.check_pkg()
        try:
            if not os.system('service tor start'):
                time.sleep(1)
                print('[*] CONNECTED TO TOR')
                self._renew_ip()
        except Exception as e:
            print('Oops ..!,Something went wrong')
            print(str(e))
            sys.exit()
        except KeyboardInterrupt:
            os.system('service tor stop')

    def _renew_ip(self):
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
            sys.exit('unable to connected to port 9051, [!] FAILED')

if __name__ == '__main__':
    
    passwd=input('[*] Enter the password to authenticate with tor(a password you used to create hashed password): ')

    intervals=input('[*] Enter the time to change the ip {default : 20 seconds}:')
    if intervals == '':
        intervals=20
    elif not intervals.isdigit():
        sys.exit('[!] Please enter valid input..!')
    elif int(intervals) < 20:
        sys.exit('[!] YOU ENTERED INTERVALS IS NOT PERMITTED...!, please enter the interval more than 20 seconds')
    else:
        intervals=int(intervals)

    change=input('[*] How many times you want to change the ip {maximum:200,press enter to leave default:100}: ')
    if change == '':
        change=100
    elif not change.isdigit():
        sys.exit('[!] Please enter valid input..!')
    elif int(change) > 200:
        sys.exit('[!] THIS SCRIPT ALLOW TO CHANGE IP ONLY 200 TIMES , NOT MORE THAN THAT, please enter the valid number')
    else:
        change=int(change)


    try:
        run=changeip(passwd,change,intervals)
        run._check_root()

    except KeyboardInterrupt:
        os.system('service tor stop')
        sys.exit()

