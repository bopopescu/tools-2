#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from StringIO import StringIO
import base64 

CRLF = '\n'

def mailUtf8String(base64string):
	str = "=?UTF-8?B?" + base64string + "?="
	return str

def mailUtf8QString(value): 
	str = "=".join("{:02X}".format(ord(c)) for c in value)
	str = "=?UTF-8?Q?" + str + "?="
	return str

def readFileToBase64(filename):
	fp = open(filename, "r")
	msg = fp.read()
	fp.close()
	return base64.b64encode(msg)

def execCode(code):
	print "code: ", code
	__stdout = sys.stdout
	sys.stdout = StringIO()
	exec(code)
	result = sys.stdout.getvalue()
	sys.stdout = __stdout
	return result
	
