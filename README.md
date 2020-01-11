```
   __    __  .___________..______   .______       _______   ______   ______   .__   __. 
  |  |  |  | |           ||   _  \  |   _  \     |   ____| /      | /  __  \  |  \ |  | 
  |  |__|  | `---|  |----`|  |_)  | |  |_)  |    |  |__   |  ,----'|  |  |  | |   \|  | 
  |   __   |     |  |     |   _  <  |      /     |   __|  |  |     |  |  |  | |  . `  | 
  |  |  |  |     |  |     |  |_)  | |  |\  \----.|  |____ |  `----.|  `--'  | |  |\   | 
  |__|  |__|     |__|     |______/  | _| `._____||_______| \______| \______/  |__| \__| 
                                                                                        
   Author: Cerbersec                                                                    
   Version: 1.0                                                                         
   Requires: python-nmap, gobuster, uniscan

```

### What is this?
A: A python script to combine and automate nmap, gobuster and uniscan on a HackTheBox machine, create a directory structure and write the results to log files

### But this is garbage
A: I know, feel free to improve it

### How do I use this?
A: ./htbrecon.py \<box name\> \<box ip address\>  
e.g: `./htbrecon.py Obscurity 10.10.10.168`

### What does it (or is it supposed to) do under the hood?
A: A bunch of things
1. Create a root directory \<box name\> in a location specified in the **GLOBAL CONFIG**
2. Create subdirectories for the nmap, gobuster and uniscan results
3. Add an entry in the /etc/hosts file `<box ip addres>	<box name>.htb	# created by htbrecon`
4. Run a NMAP scan `nmap -oX -T4 -A -p 1 65535`
5. Run a gobuster scan on http://\<box ip address\> using directory-list-2.3-small.txt
6. Run a gobuster scan on http://\<box ip address\> using directory-list-lowercase-2.3-small.txt
7. Run a uniscan on http://\<box ip address\>/ `uniscan -u http://<box ip address>/ -qwed`
8. Save all the output to log files: htbrecon.nmap, htbrecon.gobuster and htbrecon.uniscan 
