#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import socket
import select
import binascii
import time
import struct
import array

# total size of data (payload)
ICMP_DATA_STR = 56  

# initial values of header variables
ICMP_TYPE = 8
ICMP_TYPE_IP6 = 128
ICMP_CODE = 0
ICMP_CHECKSUM = 0
ICMP_ID = 0
ICMP_SEQ_NR = 0

# Package definitions.
__program__   = 'ping'
__version__   = '0.5a'
__date__      = '2004/15/12'
__author__    = 'Lars Strand ;'
__licence__   = 'GPL'
__copyright__ = 'Copyright (C) 2004 Lars Strand'

def _construct(id, size, ipv6):
    """Constructs a ICMP echo packet of variable size
    """

    # size must be big enough to contain time sent
    if size < int(struct.calcsize("d")):
        _error("packetsize to small, must be at least %d" % int(struct.calcsize("d")))
   
    # construct header
    if ipv6:
        header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, ICMP_CHECKSUM, \
                             ICMP_ID, ICMP_SEQ_NR+id)
    else:
        header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, ICMP_CHECKSUM, \
                             ICMP_ID, ICMP_SEQ_NR+id)

    # if size big enough, embed this payload
    load = "-- IF YOU ARE READING THIS YOU ARE A NERD! --"
   
    # space for time
    size -= struct.calcsize("d")

    # construct payload based on size, may be omitted :)
    rest = ""
    if size > len(load):
        rest = load
        size -= len(load)

    # pad the rest of payload
    rest += size * "X"

    # pack
    data = struct.pack("d", time.time()) + rest
    packet = header + data          # ping packet without checksum
    checksum = _in_cksum(packet)    # make checksum

    # construct header with correct checksum
    if ipv6:
        header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, checksum, \
                             ICMP_ID, ICMP_SEQ_NR+id)
    else:
        header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, checksum, ICMP_ID, \
                             ICMP_SEQ_NR+id)

    # ping packet *with* checksum
    packet = header + data

    # a perfectly formatted ICMP echo packet
    return packet


def _in_cksum(packet):
    """THE RFC792 states: 'The 16 bit one's complement of
    the one's complement sum of all 16 bit words in the header.'

    Generates a checksum of a (ICMP) packet. Based on in_chksum found
    in ping.c on FreeBSD.
    """

    # add byte if not dividable by 2
    if len(packet) & 1:              
        packet = packet + '\0'

    # split into 16-bit word and insert into a binary array
    words = array.array('h', packet)
    sum = 0

    # perform ones complement arithmetic on 16-bit words
    for word in words:
        sum += (word & 0xffff)

    hi = sum >>16
    lo = sum & 0xffff
    sum = hi + lo
    sum = sum + (sum >> 16)
   
    return (~sum) & 0xffff # return ones complement


def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff 
        count = count + 2
    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff 
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def ping(host):

    ipv6 = 0

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
    #packet = struct.pack(
    #        "!BBHHH", 8, 0, 0, 0, 0
    #)
    #chksum=checksum(packet)
    #packet = struct.pack(
    #        "!BBHHH", 8, 0, chksum, 0, 0
    #)

    alive = 0
    start = 1
    size = ICMP_DATA_STR
    packet = _construct(start, size, ipv6) # make a ping packet
    s.sendto(packet, (host, 1))

    ip = socket.gethostbyname(host)

    pong = ""; iwtd = []
    timeout = 2
    # wait until there is data in the socket
    while 1:
        # input, output, exceptional conditions
        iwtd, owtd, ewtd = select.select([s], [], [], timeout)
        break # no data and timout occurred

    if iwtd:  # ok, data on socket
        endtime = time.time()  # time packet received
        pong, address = s.recvfrom(size+48)

        #print "length 'pong': %d" % len(pong)
        if len(pong) < 36:
            return -1

        if ipv6:
            # fetch pong header
            pongHeader = pong[0:8]
            pongType, pongCode, pongChksum, pongID, pongSeqnr = \
                      struct.unpack("bbHHh", pongHeader)

            # fetch starttime from pong
            starttime = struct.unpack("d", pong[8:16])[0]

        # IPv4
        else:

            # time to live
            rawPongHop = struct.unpack("s", pong[8])[0]

            # convert TTL from 8 bit to 16 bit integer
            pongHop = int(binascii.hexlify(str(rawPongHop)), 16)

            # fetch pong header
            pongHeader = pong[20:28]
            pongType, pongCode, pongChksum, pongID, pongSeqnr = \
                      struct.unpack("bbHHh", pongHeader)

            # fetch starttime from pong
            starttime = struct.unpack("d", pong[28:36])[0]

        # valid ping packet received?
        if not pongSeqnr == start:
            pong = None

    # NO data on socket - timeout waiting for answer
    if not pong:
        #if alive:
        #    print "no reply from %s (%s)" % (str(host), str(ip))
        #else:
        #    print "ping timeout: %s (icmp_seq=%d) " % (ip, start)
        return -1

    triptime = (endtime - starttime) * 1000 # compute RRT
    #print "time: %.2f (ms)" % triptime 
    return triptime

	
def average_ping(host, n=3):
	total = 0.0
	lost = 0
	for i in range(n):
		#print i
		ms = ping(host)
		#print "%f (ms)" % ms
		if ms > 0:
			total += ms
		else:
			lost += 1
	
	#print "total: %f" % total
	#print "average time: %.2f (ms), %d lost" % (total / n, lost)
	if lost > 0:
		return -1
	else:
		return (total / n)

if __name__=='__main__':
	#ping('192.168.41.56')
	triptime = average_ping(sys.argv[1])
	print "average trip time: %.2f (ms)" % triptime
