#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os 
import sys 
import string
import commands

mysqlstr = "mysql -uroot -ptango9896 google_ip -e"
history_table = "history_ips"
available_table = "available_ips"

def is_valid_ip(ip):
	return True

def ip_str_clean(ip):
	ip = ip.strip(' ')
	ip = ip.strip('\n')
	ip = ip.strip('\r')
	return ip

def add_to_db(ip):
	if is_valid_ip(ip) == False:
		return False

	sql = "insert into %s (ip) values ('%s')" % (history_table, ip)
	cmd = "%s \"%s\"" % (mysqlstr, sql)
	#print cmd

	result = commands.getstatusoutput(cmd)
	if result[0] != 0:
		print result[1]

def get_ip_from_file(filename):
	f = open(filename)

	while 1:
		line = f.readline()
		if not line:
			break

		#print "line: %s" % line

		if line.find('|') >= 0:
			ips = line.split('|')
		elif line.find(',') >= 0:
			ips = line.split(',')
		elif line.find(' ') >= 0:
			ips = line.split(' ')
		else:
			ips = line

		for ip in ips:
			if len(ip) > 6:
				#print "ip: %s" % ip
				ip = ip_str_clean(ip)
				#print ip
				add_to_db(ip)
		#break


if len(sys.argv) != 2:
	print "Usage: %s <file>" % sys.argv[0]
	exit()

get_ip_from_file(sys.argv[1])
