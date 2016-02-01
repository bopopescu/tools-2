#!/usr/bin/python
# -*- coding: utf-8 -*-

import com
import base64
import time 
#import md5
import random

#	getContentType()
#	getBoundary()
#	getMessageBody()


def getContentType():
	return content_type

def getBoundary():
	return boundary

def getMessageBody():
	return message

def randomString():
	num = (int)(random.random() * 100)
	str = time.ctime() + " - dscloud - " + hex(num)
	return base64.b64encode(str)

class EmailImage(object):
	cid = 1
	@staticmethod
	def addImage(self, imagefile):
		suffix = imagefile.split(".")[1]
		#suffix = 'jpeg'
		content_id = "atuomail_" + str(self.cid) + "_@dscloud"
	
		msg = "Content-Type: image/" + suffix + "; name=\"" + imagefile + "\"\n" \
			+ "Content-Transfer-Encoding: base64\n" \
			+ "Content-Disposition: inline; filename=\"" + imagefile + "\"\n" \
			+ "Content-ID: <" + content_id + ">\n" \
			+ "\n" \
			+ com.readFileToBase64(imagefile) 
		self.cid += 1
		result = {'cid':content_id, 'content':msg}
		return result


content_type = "multipart/related"

boundary = "dscloud-automail-0123456789"

imgres1 = EmailImage.addImage(EmailImage, "ds-logo-1.2.png")
imgres2 = EmailImage.addImage(EmailImage, "web_sample_2.png")

message_body = """
<html>
<body style="width:600px;">
<head>
<title></title>
</head>

<div>打赏，新兴互联网付费模式，还要错过吗？</div>
<div style="color:white">""" + randomString() + """</div>
<br/>
<div style="width:100%;height:32px;text-align:center;">
<img style="height:32px;position:relative;float:left;padding-left:160px" src="cid:""" + imgres1['cid'] + """" />
<div style="height:32px;color:#13afeb;font-size:32px;position:relative;float:left;padding-left:10px;">
<a style="color:#13afeb;text-decoration:none;" href="http://www.dashangcloud.com">云打赏</a>
</div>
</div>

<div style="text-align:left;padding-top:10px;padding-left:145px">
<div><a style="color:#13afeb;text-decoration:none;" href="http://www.dashangcloud.com">www.dashangcloud.com</a></div>
</div>
<br/>

<div style="text-align:left;padding-left:20px;">
<h5>
打赏是互联网新兴的一种非强制性的付费模式，具有很好的用户体验。
</h5>

<h4>云打赏为您实现打赏：</h4>

<div style="text-align:left;padding-left:40px;">
<h3>1.一行代码让您的网站支持打赏</h3>
<h3>2.一个链接让您在任何地方支持打赏</h3>
<h3>3.支持支付宝和微信支付</h3>
</div>

</div>

<div style="color:white">""" + randomString() + """</div>


<h4>实例：</h4>
<img style="" src="cid:""" + imgres2['cid'] + """" />
</body>
</html>

<div style="color:white">""" + randomString() + """</div>

<div><a style="color:#13afeb;text-decoration:none;" href="http://www.dashangcloud.com">了解更多...</a></div>
"""

message = """--"""+ boundary + """
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: base64

""" + base64.b64encode(message_body) + """

--""" + boundary + """
""" + imgres1['content'] + """

--""" + boundary + """
""" + imgres2['content'] + """

--""" + boundary + """--
"""

