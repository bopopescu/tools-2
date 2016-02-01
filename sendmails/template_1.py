#!/usr/bin/python
# -*- coding: utf-8 -*-

import com
import base64

#	getContentType()
#	getBoundary()
#	getMessageBody()


def getContentType():
	return content_type

def getBoundary():
	return boundary

def getMessageBody():
	return message

cid = 1
def addImage(imagefile):
	suffix = imagefile.split(".")[1]
	#suffix = 'jpeg'
	content_id = "atuomail_" + str(cid) + "_@dscloud"

	msg = "Content-Type: image/" + suffix + "; name=\"" + imagefile + "\"\n" \
		+ "Content-Transfer-Encoding: base64\n" \
		+ "Content-Disposition: inline; filename=\"" + imagefile + "\"\n" \
		+ "Content-ID: <" + content_id + ">\n" \
		+ "\n" \
		+ com.readFileToBase64(imagefile) 
	++cid
	result = {'cid':content_id, 'content':msg}
	return result


content_type = "multipart/related"

boundary = "dscloud-automail-0123456789"

imgres = addImage("xl.jpg")
#imgres = addImage("ds.png")

message_body = """
<h3>Hello world.</h3>
<DIV><IMG src="cid:""" + imgres['cid'] + """"></DIV>
<h5>如何让字一连串，这样就行了啦~~</h5>
"""

message = """--"""+ boundary + """
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: base64

""" + base64.b64encode(message_body) + """

--""" + boundary + """
""" + imgres['content'] + """

--""" + boundary + """--
"""

