#!/usr/bin/python
#-*-coding: utf-8-*-

import socket
import sys

def scanner(target, ports = range(0,65536)):
  for i in ports:
		s = socket.socket()
		s.settimeout(0.1)
		serv = ""
		if s.connect_ex((target, i)) == 0:
			try:
				serv = socket.getservbyport(i)
			except:
				serv = ""
			yield i, serv
		s.close()

def target_ip(target):
	if len(target.split(".")) == 4:
		cnt = 0
		for i in target.split("."):
			if i.isdigit() and int(i) <= 255:
				cnt += 1
			if cnt == 4:
				return True
	return False

def main(argc, argv):
	if argc != 2:
		print "Usage:", argv[0], "target"
		return
	target = argv[1]
	if not target_ip(target):
		try:
			target = socket.gethostbyname(target)
		except:
			return 1
	for i in scanner(target):
		print i
	return 0

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
