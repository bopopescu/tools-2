#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

class QNum:
	user = 'root'
	password = '123456'
	host = '127.0.0.1'
	database = 'qqnum_test'

	dbconn = None
	dbcursor = None
	query = ''

	#min_count = 0

	def __init__(self):
		self.dbconn = mysql.connector.connect(
							user = self.user, 
							password = self.password, 
							host = self.host, 
							database = self.database)
		self.dbcursor = self.dbconn.cursor()

	def get_a_num(self):
		min_count = self.get_min_count()
		query = ('select qq_qun, qq_no from qq_no where apply_count = %d limit 1') % min_count
		self.dbcursor.execute(query)
		row = {'qq_qun' : '', 'qq_num' : ''}
		(row['qq_qun'], row['qq_num']) = self.dbcursor.fetchone()
		return row

	def get_a_num(self, min_count):
		try:
			query = ('select qq_qun, qq_no from qq_no where apply_count = %d limit 1') % min_count
			self.dbcursor.execute(query)
			row = {'qq_qun' : '', 'qq_num' : ''}
			(row['qq_qun'], row['qq_num']) = self.dbcursor.fetchone()
			return row
		except (mysql.connector.Error, TypeError) as err:
			#print("errno: %d, errmsg: %s") % err.errno, err
			return None
		else:
			print "unknow error"

	def num_count(self, qq_qun, qq_num):
		query = ('update qq_no set apply_count = apply_count + 1 where qq_qun = "%s" and qq_no = "%s"') % (qq_qun, qq_num)
		self.dbcursor.execute(query)
		result = self.dbcursor.fetchone()
		self.dbconn.commit() # notice this statement
		

	def get_min_count(self):
		query = ('select min(apply_count) as min_count from qq_no')
		self.dbcursor.execute(query)
		return self.dbcursor.fetchone()

def test2():
	qn = QNum()
	row = qn.get_a_num()
	print ("in test2, row: %s") % row 
	print row
	#row = {'qq_qun' : '550605', 'qq_num' : '7787677'}
	qn.num_count(row['qq_qun'], row['qq_num'])

def test1():
	try:
		cnx = mysql.connector.connect(user='root'
				,password='123456'
				,host='127.0.0.1'
				,database='qqnum'
			)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cnx.close()

#test1()
#test2()
