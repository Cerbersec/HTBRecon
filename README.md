```
   __    __  .___________..______   .______       _______   ______   ______   .__   __. 
  |  |  |  | |           ||   _  \  |   _  \     |   ____| /      | /  __  \  |  \ |  | 
  |  |__|  | `---|  |----`|  |_)  | |  |_)  |    |  |__   |  ,----'|  |  |  | |   \|  | 
  |   __   |     |  |     |   _  <  |      /     |   __|  |  |     |  |  |  | |  . `  | 
  |  |  |  |     |  |     |  |_)  | |  |\  \----.|  |____ |  `----.|  `--'  | |  |\   | 
  |__|  |__|     |__|     |______/  | _| `._____||_______| \______| \______/  |__| \__| 
                                                                                        
   Author: Cerbersec                                                                    
   Version: 1.0                                                                         
   Requires: nmap, gobuster, uniscan

```

### What is this?
A: A python script to combine and automate nmap, gobuster and uniscan on a HackTheBox machine, create a directory structure and write the results to log files

### But this is garbage
A: I know, feel free to improve it

### How do I use this?
```
usage: HTBRecon [options] box_name box_address

Create a directory structure and perform a series of scans on a target

positional arguments:
  box_name             target name: used to create the directory structure
  box_address          target ip address

optional arguments:
  -h, --help           show this help message and exit
  -q, --quick          determine scan parameters: nmap -Pn -sV; gobuster http
                       small wordlists; uniscan -q -w
  -c, --comprehensive  determine scan parameters: nmap -T4 -A -p 1-65535;
                       gobuster http/https medium wordlists; uniscan -q -w -e
                       -d
  -x, --https          force https
  --version            show program's version number and exit  
```

### What does it (or is it supposed to) do under the hood?
A: A bunch of things

1. Create a root directory \<box name\> in a location specified in the **GLOBAL CONFIG**
2. Create subdirectories for the nmap, gobuster and uniscan results
3. Add an entry in the /etc/hosts file `<box ip addres>	<box name>.htb	# created by htbrecon`
4. Run a NMAP scan
   1. Quick scan: `nmap -Pn -sV`
   2. Default scan: `nmap -sC -sV`
   3. Comprehensive scan: `nmap -T4 -A -p 1-65535
5. Run a gobuster scan
   1. Quick scan: http, small wordlist
   2. Default: http(s), small wordlist
   3. Comprehensive: http and https, medium wordlist
7. Run a uniscan
   1. Quick scan: `uniscan -qw`
   2. Default scan: `uniscan -qwe`
   3. Comprehensive scan: `uniscan -qwed`
8. Save all the output to log files
   1. nmap: htbrecon.nmap
   2. gobuster: htbrecon.gobuster
   3. uniscan: \<box ip address\>.html
