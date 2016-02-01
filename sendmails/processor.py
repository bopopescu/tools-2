#!/usr/bin/python
# -*- coding: utf-8 -*-

from db import QNum
from smtp import MySmtp
import time
import logging

#
#	configuration
#

send_interval = 5 # seconds


#
#	main process function
# 

def run():
	#print "Hello from run",
	qn = QNum()
	min_count = qn.get_min_count()


	while True:
		print "while loop in run"
		row = qn.get_a_num(min_count)
		if row is None:
			break

		print row
		# send mail
		qmail_addr = row['qq_num'] + "@qq.com"
		print qmail_addr

		#ms = MySmtp("1485084328@qq.com", "", "smtp.qq.com")
		#ms = MySmtp("1533493816@qq.com", "becktu123", "smtp.qq.com")
		ms = MySmtp("2305621863@qq.com", "dashang987", "smtp.qq.com")

		ms.addReceiver(qmail_addr)
		ms.setSenderName("云打赏")
		ms.setSubject("云打赏，一行代码让您的网站支持打赏！")
		ms.setTemplate("template_first_tui")
		ms.sendSeparatedOneConnection()


		# log
		#logging.info("log %s %s %d", row)

		# update database
		qn.num_count(row['qq_qun'], row['qq_num'])
		time.sleep(send_interval)


if __name__ == "__main__":
	print "E-mail Sender."
	run()
