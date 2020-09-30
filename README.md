# ip-changer

###DESCRIPTION:
        This IP-CHANGER tool is designed  for linux user (root user only) and this tool changes ip address and privides annonymity while browsing.
        Using my tool you can set intervals to change ip adress and is restricted to use intervals
        above 20 seconds ,and is restricted change ip address only for 200 times (soon i wiill update for more than 200 times)
        
USAGE:
       Before running this tool , you have to edit torrc(tor configure file ) file. 
       You get this in /etc/tor directory.

       FOLLOW BELLOW STEPS TO EDIT TORRC FILE CORRECTLY:
       
       STEP 1: change directory to tor(/etc/tor) ,open torrc file and uncomment ControlPort 9051,
               and HashedControlPassword
       STEP 2: open new terminal and type ' tor --hash-password <enter password> , This creates hashed passowrd 
        
       STEP 3: Now paste hashed password in torrc file . ie HashedControlPassword <paste created hashed password> , and save the changes
       
       STEP 4: Now open browser setting --> Network settings --> choose manual proxy configuration --> SOCKS Host 127.0.0.1 , PORT 9050
               now save the changes 
               
       STEP 4: Run script
`python3 ipchanger.py`

