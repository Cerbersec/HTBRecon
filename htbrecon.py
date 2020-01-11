#!/usr/bin/env python3

import os
import sys

import argparse

import subprocess
from multiprocessing import Process, Queue

from pathlib import Path


def init_config():
	global OUTPUT_DIR = "/root/Desktop/HackTheBox/HackTheBox/"
	global OUTPUT_DIR_NMAP = "/nmap"
	global OUTPUT_DIR_GOBUSTER = "/gobuster"
	global OUTPUT_DIR_UNISCAN = "/uniscan"

	global APPEND_HOSTS = True

	global NMAP_BIN_LOC = "/usr/bin/nmap"
	global GOBUSTER_BIN_LOC = "/usr/bin/gobuster"
	global UNISCAN_BIN_LOC = "/usr/bin/uniscan"

	global DIR_SMALL = "/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt"
	global DIR_SMALL_LOWER = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-small.txt"
	global DIR_MEDIUM = "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt"
	global DIR_MEDIUM_LOWER = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt"

	global NMAP_ARGS_DEFAULT = "-sC -sV"
	global NMAP_ARGS_QUICK = "-Pn -sV"
	global NMAP_ARGS_COMPR = "-T4 -A -p 1-65535"

	global UNISCAN_ARGS_DEFAULT = "-qwe"
	global UNISCAN_ARGS_QUICK = "-qw"
	global UNISCAN_ARGS_COMPR = "-qwed"

	global VERSION = "1.0"


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
			f.write("\n" + box_name.lower() + "\t" + box_address + ".htb \t# created by htbrecon")
			f.close()
		except:
			print("|error| insufficient permissions: could not write to /etc/hosts")

def launch_nmap(box_name, box_address, args):
	try:
		out = OUTPUT_DIR + box_name + OUTPUT_DIR_NMAP + "/htbrecon"
		nmap_process = subprocess.call([NMAP_BIN_LOC, args, "-oN", out, box_address])
		print(nmap_process)
	except:
		print("|error| failed to initiate nmap")

def launch_gobuster(box_name, box_address, wordlist, force_https):
	set_http = "http://"
	if force_https:
		set_http = "https://"

	try:
		out = OUTPUT_DIR + box_name + OUTPUT_DIR_GOBUSTER + "/htbrecon.gobuster"
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
	if force_https:
		set_http = "https://"
	try:
		out = OUTPUT_DIR + box_name + OUTPUT_DIR_UNISCAN + "/htbrecon.uniscan"
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


def main(args):
	print_banner()

	print("|start| creating directories")
	initialize(args.box_name)

	print("|start| creating hosts entry")
	configure_hosts(args.box_name, args.box_address)

	print("|start| starting nmap")
	if args.q:
		launch_nmap(args.box_name, args.box_address, NMAP_ARGS_QUICK)
	elif args.c:
		launch_nmap(args.box_name, args.box_address, NMAP_ARGS_COMPR)
	else:
		launch_nmap(args.box_name, args.box_address, NMAP_ARGS_DEFAULT)

	print("|start| starting gobuster")
	if args.q:
		launch_gobuster(args.box_name, args.box_address, DIR_SMALL, args.x)
	elif args.c:
		launch_gobuster(args.box_name, args.box_address, DIR_MEDIUM, False)
		launch_gobuster(args.box_name, args.box_address, DIR_MEDIUM, True)
	else:
		launch_gobuster(args.box_name, args.box_address, DIR_MEDIUM, args.x)

	print("|start| starting uniscan")
	if args.q:
		launch_uniscan(args.box_name, args.box_address, UNISCAN_ARGS_QUICK, args.x)
	elif args.c:
		launch_uniscan(args.box_name, args.box_address, UNISCAN_ARGS_COMPR, args.x)
	else:
		launch_uniscan(args.box_name, args.box_address, INISCAN_ARGS_DEFAULT, args.x)

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





