#!/usr/bin/env python3

import os
import sys
from . imports utils

#import argparse

import subprocess
from multiprocessing import Process, Queue

from pathlib import Path

import nmap

#||===== GLOBAL CONFIG =====||

# direcory where htbrecon will create individual directories for each box
OUTPUT_DIR = "/root/Desktop/HackTheBox/HackTheBox/"

# output_dir + box_name + output_[nmap | gobuster | uniscan]
OUTPUT_NMAP = "/nmap"
OUTPUT_GOBUSTER = "/gobuster"
OUTPUT_UNISCAN = "/uniscan"

# append box to /etc/hosts file
APPEND_HOSTS = True

# gobuster location
GOBUSTER_LOC = "/usr/bin/gobuster"

#uniscan location
UNISCAN_LOC = "/usr/bin/uniscan"

# wordlists
DIR_SMALL = "/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt"
DIR_SMALL_LOWER = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-small.txt"

#||===== END OF CONFIG =====||



def print_banner():
	print("   __    __  .___________..______   .______       _______   ______   ______   .__   __. ")
	print("  |  |  |  | |           ||   _  \  |   _  \     |   ____| /      | /  __  \  |  \ |  | ")
	print("  |  |__|  | `---|  |----`|  |_)  | |  |_)  |    |  |__   |  ,----'|  |  |  | |   \|  | ")
	print("  |   __   |     |  |     |   _  <  |      /     |   __|  |  |     |  |  |  | |  . `  | ")
	print("  |  |  |  |     |  |     |  |_)  | |  |\  \----.|  |____ |  `----.|  `--'  | |  |\   | ")
	print("  |__|  |__|     |__|     |______/  | _| `._____||_______| \______| \______/  |__| \__| ")
	print("                                                                                        ")
	print("   Author: Cerbersec                                                                    ")
	print("   Version: 1.0                                                                         ")
	print("   Requires: python-nmap, gobuster, uniscan                                             ")

def initialize(box_name):
	p = Path(OUTPUT_DIR + box_name)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

	p = Path(OUTPUT_DIR + box_name + OUTPUT_NMAP)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

	p = Path(OUTPUT_DIR + box_name + OUTPUT_GOBUSTER)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

	p = Path(OUTPUT_DIR + box_name + OUTPUT_UNISCAN)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

def configure_hosts(box_name, box_address):
	if APPEND_HOSTS:
		try:
			f = open("/etc/hosts", "a")
			f.write("\n" + box_name.lower() + "\t" + box_address + ".htb\t# created by htbrecon")
			f.close()
		except:
			print("|error| insufficient permissions: could not write to /etc/hosts")

def launch_nmap(box_name, box_address):
	nm = nmap.PortScanner()
	try:
		nm.scan(hosts = box_address, arguments = '-T4 -A -p 1-65535')
		try:
			f = open(OUTPUT_DIR + box_name + OUTPUT_NMAP + "/htbrecon.nmap", "w")
			f.write("Scan results for: " + box_address + "\r\n")
			f.write("=====================================\r\n")
			for proto in nm[box_address].all_protocols():
				f.write("Protocol: " + proto)
				lport = nm[box_address][proto].keys()
				lport.sort()
				for port in lport:
					f.write("port: " + port + " " + nm[box_address][proto][port]['state'] + " " +  nm[box_address][proto]['name'] + " " + nm[box_address][proto]['product'] + " " + nm[box_address][proto]['extrainfo'] + " " + nm[box_address][proto]['version'])
			
			f.close()
			print("|info| nmap scan: finished")
		except Exception as e:
			print("|error| insufficient permissions: failed to write nmap result")
			print(e)
	except Exception as ex:
		print("|error| failed to initiate nmap scan")
		print(ex)
	

def launch_gobuster(box_name, box_address, wordlist):
	try:
		process = subprocess.run([GOBUSTER_LOC, "dir", "-w", "wordlist", "-x", ".php", "-u", "http://" + box_address], capture_output=True)
		try:
			f = open(OUTPUT_DIR + box_name + OUTPUT_GOBUSTER + "/htbrecon.gobuster", "w")
			f.write(utils.decode_utf8(process.stdout))
			f.close()
			print("|info| gobuster: finished")
		except:
			print("|error| insufficient permissions: failed to write gobuster result")
	except:
		print("|error| failed to initiate gobuster")


def launch_uniscan(box_name, box_address):
	try:
		process = subprocess.run([UNISCAN_LOC, "-u", "http://" + box_address + "/", "-qwed"], capture_output=True)
		try:
			f = open(OUTPUT_DIR + box_name + OUTPUT_UNISCAN + "/htbrecon.uniscan", "w")
			f.write(utils.decode_utf8(process.stdout))
			f.close()
			print("|info| uniscan: finished")
		except Exception as e:
			print("|error| insufficient permissions: failed to write uniscan result")
			print(e)
	except:
		print("|error| failed to initiate uniscan")



def main(argv):
	print_banner()

	if len(argv) > 1:
		print("|start| creating directories")
		initialize(argv[1])

		print("|start| creating hosts entry")
		configure_hosts(argv[1], argv[2])

		print("|start| starting nmap")
#		launch_nmap(argv[1], argv[2])
		p_nmap = Process(target = launch_nmap, args=(argv[1], argv[2]))
		p_nmap.start()

		print("|start| starting gobuster")
#		launch_gobuster(argv[1], argv[2], DIR_SMALL)
#		launch_gobuster(argv[1], argv[2], DIR_SMALL_LOWER)
		p_gobuster = Process(target = launch_gobuster, args=(argv[1], argv[2], DIR_SMALL))
		p_gobuster.start()

		p_gobuster_lower = Process(target = launch_gobuster, args=(argv[1], argv[2], DIR_SMALL_LOWER))
		p_gobuster_lower.start()

		print("|start| starting uniscan")
#		launch_uniscan(argv[1], argv[2])
		p_uniscan = Process(target = launch_uniscan, args=(argv[1], argv[2]))
		p_uniscan.start()

		p_nmap.join()
		p_gobuster.join()
		p_gobuster_lower.join()
		p_uniscan.join()

		print("|info| all scans complete")
	else:
		print("|error|===== aborting: missing arguments <box name> <box ip address>  =====||")
	

if __name__ == "__main__":
	main(sys.argv)


