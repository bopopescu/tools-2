#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import commands
from seek_config import history_table 
from seek_config import mysqlstr
from icmp_echo_request import average_ping

def get_min_detect_count():

	sql = "select min(detect_count) from %s" % history_table
	cmd = "%s \"%s\"" % (mysqlstr, sql)
	#print cmd

	result = commands.getstatusoutput(cmd)
	if result[0] != 0:
		print result[1]

def clean_overdue_available_ip():
	return True


def enter(index):
	#print "enter with index: %d" % index
	start = index
	amount = 100
	while True:
		sql = "select ip from %s limit %d,%d" % (history_table, start, amount)
		cmd = "%s \"%s\"" % (mysqlstr, sql)
		#print cmd

		result = commands.getstatusoutput(cmd)
		#print result

		if len(result[1]) < 1:
			break

		ips = result[1].split('\n')
		for ip in ips:
			if ip == "ip":
				continue		
			#print ip
			ms = average_ping(ip)	
			#print "%-15s %.2f" % (ip, ms)
			if ms < 0:
				continue
			print "%-15s %.2f" % (ip, ms)

		#break

		start += amount


if __name__=='__main__':
	index=1
	if len(sys.argv) != 2:
		print "Usage: %s <index>" % sys.argv[0]
		print "Default index = 1"
	else:
		index = atoi(sys.argv[1])
		print "index = %d" % index
		
	enter(index)
