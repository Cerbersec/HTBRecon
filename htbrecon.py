#!/usr/bin/env python3

import os
import sys
import socket

import argparse

import subprocess
from multiprocessing import Process, Queue

from pathlib import Path

########## GLOBAL CONFIG ##########

OUTPUT_DIR = "/root/Desktop/HackTheBox/HackTheBox/"
OUTPUT_DIR_NMAP = "/nmap"
OUTPUT_DIR_GOBUSTER = "/gobuster"
OUTPUT_DIR_UNISCAN = "/uniscan"

APPEND_HOSTS = True

NMAP_BIN_LOC = "/usr/bin/nmap"
GOBUSTER_BIN_LOC = "/usr/bin/gobuster"
UNISCAN_BIN_LOC = "/usr/bin/uniscan"

DIR_SMALL = "/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt"
DIR_SMALL_LOWER = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-small.txt"
DIR_MEDIUM = "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt"
DIR_MEDIUM_LOWER = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt"

NMAP_ARGS_DEFAULT = ["-sC", "-sV"]
NMAP_ARGS_QUICK = ["-Pn", "-sV"]
NMAP_ARGS_COMPR = ["-T4", "-A", "-p", "1-65535"]

UNISCAN_ARGS_DEFAULT = "-qwe"
UNISCAN_ARGS_QUICK = "-qw"
UNISCAN_ARGS_COMPR = "-qwed"

VERSION = "1.0"

########## END OF CONFIG ##########

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

	p = Path(OUTPUT_DIR + box_name + OUTPUT_DIR_NMAP)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

	p = Path(OUTPUT_DIR + box_name + OUTPUT_DIR_GOBUSTER)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

	p = Path(OUTPUT_DIR + box_name + OUTPUT_DIR_UNISCAN)
	try:
		p.mkdir()
	except FileExistsError as e:
		print("|info| skipping: directory already exists")

def configure_hosts(box_name, box_address):
	if APPEND_HOSTS:
		try:
			f = open("/etc/hosts", "a")
			f.write("\n" + box_address + "\t" + box_name.lower() + ".htb \t# created by htbrecon")
			f.close()
		except:
			print("|error| insufficient permissions: could not write to /etc/hosts")

def launch_nmap(box_name, box_address, quick, compr):
	try:
		out = OUTPUT_DIR + box_name + OUTPUT_DIR_NMAP + "/htbrecon"

		if quick:
			nmap_process = subprocess.call([NMAP_BIN_LOC, "-Pn", "-sV", "-oN", out, box_address])
		elif compr:
			nmap_process = subprocess.call([NMAP_BIN_LOC, "-T4", "-A", "-p", "1-65535", "-oN", out, box_address])
		else:
			nmap_process = subprocess.call([NMAP_BIN_LOC, "-sC", "-sV", "-oN", out, box_address])
		print(nmap_process)
	except Exception as e:
		print("|error| failed to initiate nmap")
		print(e)

def launch_gobuster(box_name, box_address, wordlist, force_https):
	set_http = "http://"
	prefix = "http_"
	if force_https:
		set_http = "https://"
		prefix = "https_"

	try:
		out = OUTPUT_DIR + box_name + OUTPUT_DIR_GOBUSTER + "/" + prefix + "htbrecon.gobuster"
		gobuster_process = subprocess.call([GOBUSTER_BIN_LOC, "dir", "-w", wordlist, "-x", ".php", "-o", out, "-u", set_http + box_address])
#		try:
#			f = open(out, "w")
#			f.write(gobuster_process.stdout)
#			f.close()
#			print("|info| gobuster: finished")
#		except:
#			print("|error| insufficient permissions: failed to write gobuster result")
		print(gobuster_process)
	except:
		print("|error| failed to initiate gobuster")


def launch_uniscan(box_name, box_address, args, force_https):
	set_http = "http://"
	prefix = "http_"
	if force_https:
		set_http = "https://"
		prefix = "https_"
	try:
		out = OUTPUT_DIR + box_name + OUTPUT_DIR_UNISCAN + "/" + prefix + "htbrecon.uniscan"
		uniscan_process = subprocess.call([UNISCAN_BIN_LOC, "-u", set_http + box_address + "/", args])
#		try:
#			f = open(out, "w")
#			f.write(uniscan_process.stdout)
#			f.close()
#			print("|info| uniscan: finished")
#		except Exception as e:
#			print("|error| insufficient permissions: failed to write uniscan result")
#			print(e)
		print(uniscan_process)
	except:
		print("|error| failed to initiate uniscan")


def check_port(box_address, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)
	res = sock.connect_ex((box_address, port))
	if res == 0:
		return True
	else:
		return False

def main(args):
	print_banner()

	print("|start| creating directories")
	initialize(args.box_name)

	print("|start| creating hosts entry")
	configure_hosts(args.box_name, args.box_address)

	print("|start| starting nmap")
	launch_nmap(args.box_name, args.box_address, args.quick, args.comprehensive)

	print("|start| starting gobuster")
	if args.quick:
		if check_port(args.box_address, 80) and not args.https or check_port(args.box_address, 443) and args.https:
			launch_gobuster(args.box_name, args.box_address, DIR_SMALL, args.https)
		else:
			print("|info| failed to start gobuster: port closed")
	elif args.comprehensive:
		if check_port(args.box_address, 80):
			launch_gobuster(args.box_name, args.box_address, DIR_MEDIUM, False)
		else:
			print("|info| failed to start gobuster: port 80 closed")
		if check_port(args.box_address, 443):
			launch_gobuster(args.box_name, args.box_address, DIR_MEDIUM, True)
		else:
			print("|info| failed to start gobuster: port 443 closed")
	else:
		if check_port(args.box_address, 80) and not args.https or check_port(args.box_address, 443) and args.https:
			launch_gobuster(args.box_name, args.box_address, DIR_MEDIUM, args.https)
		else:
			print("|failed to start gobuster: port closed")

	print("|start| starting uniscan")
	if args.quick:
		if check_port(args.box_address, 80) and not args.https or check_port(args.https, 443) and args.https:
			launch_uniscan(args.box_name, args.box_address, UNISCAN_ARGS_QUICK, args.https)
		else:
			print("|info| failed to start uniscan: port closed")
	elif args.comprehensive:
		if check_port(args.box_address, 80):
			launch_uniscan(args.box_name, args.box_address, UNISCAN_ARGS_COMPR, False)
		else:
			print("|info| failed to start uniscan: port 80 closed")
		if check_port(args.box_address, 443):
			launch_uniscan(args.box_name, args.box_address, UNISCAN_ARGS_COMPR, True)
		else:
			print("|info| failed to start uniscan: port 443 closed")
	else:
		if check_port(args.box_address, 80) and not args.https or check_port(args.box_address, 443) and args.https:
			launch_uniscan(args.box_name, args.box_address, UNISCAN_ARGS_DEFAULT, args.https)
		else:
			print("|info| failed to start uniscan: port closed")

	print("|info| all scans complete")
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='HTBRecon', usage='%(prog)s [options] box_name box_address', description='Create a directory structure and perform a series of scans on a target')
	parser.version = VERSION
	parser.add_argument('box_name', metavar='box_name', type=str, help='target name: used to create the directory structure')
	parser.add_argument('box_address', metavar='box_address', type=str, help='target ip address')
	parser.add_argument('-q', '--quick', action='store_true', help='determine scan parameters: nmap -Pn -sV; gobuster http small wordlists; uniscan -q -w')
	parser.add_argument('-c', '--comprehensive', action='store_true', help='determine scan parameters: nmap -T4 -A -p 1-65535; gobuster http/https medium wordlists; uniscan -q -w -e -d')
	parser.add_argument('-x', '--https', action='store_true', help='force https')
	parser.add_argument('--version', action='version')

	args = parser.parse_args()

	main(args)





