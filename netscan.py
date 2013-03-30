#!/usr/bin/python
#-*-coding: utf-8-*-

import sys
import socket
import struct

# 192.168.2.* || 192.168.2.[1-255]
# return (192.168.2.1, 192.168.2.255)
def makeRange(argv):
  s = argv.split('.')
	e = list(s)
	if '*' in s:
		if s[3] == '*':
			s[3] = 1
			e[3] = 255
		if s[2] == '*':
			s[2] = 1
			e[2] = 255
		if s[1] == '*':
			s[1] = 1
			e[1] = 255
		if s[0] == '*':
			s[0] = 1
			e[0] = 255
	elif len(s[3].split('-')) == 2:
		r = s[3].split('-')
		s[3] = r[0][1:].strip()
		e[3] = r[1][:-1].strip()
	return ('.'.join(str(x) for x in s), '.'.join(str(x) for x in e))

# return [192.168.2.1, ..., 192.168.2.255]
def ipRange(start_ip, end_ip = None):
	l = []
	if end_ip == None:
		start_ip, end_ip = makeRange(start_ip)
	if end_ip == None:
		end_ip = start_ip
	for i in range(struct.unpack('!L', socket.inet_aton(start_ip))[0], struct.unpack('!L', socket.inet_aton(end_ip))[0] + 1):
		l += [socket.inet_ntoa(struct.pack('!L', i))]
	return l

# yield ['hostname', ['aliaslist'], ['iplist']]
def scan(ipLst):
	for i in ipLst:
		try:
			yield socket.gethostbyaddr(i)
		except:
			pass

def main(argc, argv):
	if argc == 1:
		print "Usage:", argv[0], "start-ip end-ip\nend-ip - optional"
		return
	if argc == 2:
		argv += [None]
	for host in scan(ipRange(argv[1], argv[2])):
		print host[2][0] + " - " + host[0]

if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
