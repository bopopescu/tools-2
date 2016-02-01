#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from smtplib import SMTPException
import base64 
import com 
import sys
from StringIO import StringIO
import time 
import uuid 

class MySmtp:
	host = ''
	port = ''
	sender = ''
	sendername = ''
	password = ''
	receivers = []
	subject = ''
	content_type = 'text/html; charset=UTF-8'
	message = ''
	template_file = ''
	message_body = ''
	
	CRLF = '\n'

	send_interval = 2

	def __init__(self, sender, password, host = "localhost", port = 25):
		self.sender = sender
		self.password = password
		self.sendername = sender
		self.host = host 
		self.port = port 
		self.receivers[:] = []

	def setSenderName(self, name):
		nameb64 = base64.b64encode(name)
		self.sendername = '"' + com.mailUtf8String(nameb64) + '" <' + self.sender + '>'

	def addReceiver(self, receiver):
		self.receivers.append(receiver)

	def resetReceiver(self):
		self.receiver = ()

	def setSubject(self, subject):
		subjectb64 = base64.b64encode(subject)
		self.subject = com.mailUtf8String(subjectb64)

	# without file suffix
	def setTemplate(self, template):
		self.template_file = template

	def setSendInterval(self, interval):
		self.send_interval = interval

	def newMessageID(self):
		preffix = "shang_"
		suffix = "@abcxyz.com"
		guid = uuid.uuid1()
		msgid = "<" + preffix + str(guid) + suffix + ">"
		#print msgid
		return msgid

	def buildReceivers(self):
		str = ''
		for rec in self.receivers:
			if str == '':
				str = self.buildReceiver(rec)
			else:
				str += ',' + self.buildReceiver(rec)
		return str

	def buildReceiver(self, receiver):
		str = '"' + receiver + '" <' + receiver + '>' 
		return str

	def buildMessageForAllReceiversV2(self, ctype, boundary, msg):
		all_receivers = self.buildReceivers()
		self.message = "From: " + self.sendername + self.CRLF \
			+ "To: " + all_receivers + self.CRLF \
			+ "Subject: " + self.subject + self.CRLF \
			+ "Content-Type: " + ctype + ";" + self.CRLF \
			+ "\tboundary=\"" + boundary + "\"" + self.CRLF \
			+ self.CRLF \
			+ msg \
			+ self.CRLF;
		return self.message

	def buildMessageForAllReceivers(self):
		
		mbody = ""
		ctype = ""
		boundary = ""

		__stdout = sys.stdout
		sys.stdout = StringIO()
		cmd = "import " + self.template_file
		exec(cmd)

		sys.stdout = StringIO()
		cmd = "print " + self.template_file + ".getContentType(),"
		exec(cmd)
		ctype = sys.stdout.getvalue()

		sys.stdout = StringIO()
		cmd = "print " + self.template_file + ".getBoundary(),"
		exec(cmd)
		boundary = sys.stdout.getvalue()

		sys.stdout = StringIO()
		cmd = "print " + self.template_file + ".getMessageBody(),"
		exec(cmd)
		mbody = sys.stdout.getvalue()

		sys.stdout = __stdout

		#print "[[Content Type]]: ", ctype
		#print "[[boundary]]: ", boundary

		all_receivers = self.buildReceivers()
		self.message = "From: " + self.sendername + self.CRLF \
			+ "To: " + all_receivers + self.CRLF \
			+ "Subject: " + self.subject + self.CRLF \
			+ "Content-Type: " + ctype + ";" + self.CRLF \
			+ "\tboundary=\"" + boundary + "\"" + self.CRLF \
			+ self.CRLF \
			+ mbody \
			+ self.CRLF;
		#print self.message

	def buildMessageForOneReceiver(self, receiver):

		mbody = ""
		ctype = ""
		boundary = ""

		__stdout = sys.stdout
		sys.stdout = StringIO()
		cmd = "import " + self.template_file
		exec(cmd)

		sys.stdout = StringIO()
		cmd = "print " + self.template_file + ".getContentType(),"
		exec(cmd)
		ctype = sys.stdout.getvalue()

		sys.stdout = StringIO()
		cmd = "print " + self.template_file + ".getBoundary(),"
		exec(cmd)
		boundary = sys.stdout.getvalue()

		sys.stdout = StringIO()
		cmd = "print " + self.template_file + ".getMessageBody(),"
		exec(cmd)
		mbody = sys.stdout.getvalue()

		sys.stdout = __stdout

		print "Content Type: ", self.content_type
		print "boundary: ", boundary

		all_receivers = self.buildReceiver(receiver)
		print "receiver: ", all_receivers
		self.message = "From: " + self.sendername + self.CRLF \
			+ "To: " + all_receivers + self.CRLF \
			+ "Subject: " + self.subject + self.CRLF \
			+ "Message-Id: " + self.newMessageID() + self.CRLF \
			+ "Content-Type: " + ctype + ";" + self.CRLF \
			+ "\tboundary=\"" + boundary + "\"" + self.CRLF \
			+ self.CRLF \
			+ mbody \
			+ self.CRLF;

		#all_receivers = self.buildReceiver(receiver)
		#self.message = "From: " + self.sendername + self.CRLF \
		#	+ "To: " + all_receivers + self.CRLF \
		#	+ "Subject: " + self.subject + self.CRLF \
		#	+ "Content-Type: " + self.content_type + self.CRLF \
		#	+ "\tboundary=\"" + boundary + "\"" + self.CRLF \
		#	+ self.CRLF \
		#	+ self.message_body \
		#	+ self.CRLF;
		#print self.message

	def sendSeparatedOneConnection(self):
		try:
			smtpObj = smtplib.SMTP(self.host, self.port)
			smtpObj.ehlo()
			#smtpObj.starttls()
			smtpObj.ehlo()
			smtpObj.login(self.sender, self.password)
			print "receivers count: %d" % len(self.receivers)
			for rec in self.receivers:
				self.buildMessageForOneReceiver(rec)
				smtpObj.sendmail(self.sender, rec, self.message)         
				#time.sleep(2)
			smtpObj.quit()

			print "send success."
		except SMTPException:
			print "send failed: ", sys.exc_info()[0]

	def sendSeparatedDiffConnection(self):
		try:

			for rec in self.receivers:
				smtpObj = smtplib.SMTP(self.host, self.port)
				smtpObj.ehlo()
				smtpObj.starttls()
				smtpObj.ehlo()
				smtpObj.login(self.sender, self.password)
				self.buildMessageForOneReceiver(rec)
				smtpObj.sendmail(self.sender, rec, self.message)         
				smtpObj.quit()
				#time.sleep(2)
            
			print "send success."
		except SMTPException:
			print "send failed: ", sys.exc_info()[0]

	def sendOnce(self):
		try:
			smtpObj = smtplib.SMTP(self.host, self.port)
			smtpObj.ehlo()
			smtpObj.starttls()
			smtpObj.ehlo()
			smtpObj.login(self.sender, self.password)
			self.buildMessageForAllReceivers()
			smtpObj.sendmail(self.sender, self.receivers, self.message)         
			smtpObj.quit()
			print "send success."
		except SMTPException:
			print "send failed: ", sys.exc_info()[0]



def demo1():
	try:
		#ms = MySmtp("hua_zhixing@163.com", "", "smtp.163.com")
		#ms.addReceiver("out-sky@163.com")
		#ms.addReceiver("1485084328@qq.com")

		ms = MySmtp("1485084328@qq.com", "", "smtp.qq.com")
		ms.addReceiver("519916178@qq.com")
		ms.addReceiver("out-sky@163.com")
		ms.addReceiver("hua_zhixing@163.com")

		ms.setSenderName("华")
		ms.setSubject("汉字排成行 横竖加撇捺")
		ms.setTemplate("template_1")
		#ms.sendOnce()
		ms.sendSeparated()
	except SMTPException:
		print "send failed: ", sys.exc_info()[0]

def demo2():
	try:
		ms = MySmtp("hua_zhixing@163.com", "", "smtp.163.com")
		ms.setSenderName("华")
		ms.addReceiver("1485084328@qq.com")
		ms.addReceiver("out-sky@163.com")
		ms.setSubject("汉字排成行 横竖加撇捺")
		#import template_1
		cmd = "import template_1"
		exec cmd
		#print template_1.getContentType()
		exec "msg1 = template_1.getMessageBody()"
		msg2 = ms.buildMessageForAllReceiversV2(template_1.getContentType(), template_1.getBoundary(), msg1)
		#print msg2
		#return

		smtpObj = smtplib.SMTP(ms.host, ms.port)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.ehlo()
		smtpObj.login(ms.sender, ms.password)
		smtpObj.sendmail(ms.sender, ms.receivers, ms.message)         
		smtpObj.quit()
		print "send success."
	except SMTPException:
		print "send failed: ", sys.exc_info()[0]

def demo3():
	try:
		ms = MySmtp("hua_zhixing@163.com", "", "smtp.163.com")
		ms.addReceiver("1485084328@qq.com")
		ms.setSenderName("华")
		ms.setSubject("汉字排成行 横竖加撇捺")
		ms.setTemplate("template_1")
		#ms.sendOnce()
		#ms.sendSeparated()
		ms.newMessageID()
		return

		ms = MySmtp("hua_zhixing@163.com", "", "smtp.163.com")
		ms.addReceiver("out-sky@163.com")
		ms.setSenderName("华")
		ms.setSubject("汉字排成行 横竖加撇捺")
		ms.setTemplate("template_1")
		#ms.sendOnce()
		ms.sendSeparated()
	except SMTPException:
		print "send failed: ", sys.exc_info()[0]
# ---------- #

#demo1()
#demo2()
#demo3()

