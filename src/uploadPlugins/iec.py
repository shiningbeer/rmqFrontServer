#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
 Attemts to check tcp/2404 port supporting IEC 60870-5-104 ICS protocol.
 '''

import socket
import sys,os
import threading
import time
import string
import struct
from binascii import *

BUFSIZE = 10240	#缓冲区大小10k


#if __name__ == '__main__':
def scan(ip,port = 2404):
	to_return={}
	#ip = "37.61.202.200"
	#ip = "46.23.185.39"

	
	try:
		TargetAddr = (ip, port)
	
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
		s.connect(TargetAddr)
	
		#- send TESTFR command
		#local TESTFR = string.char(0x68, 0x04, 0x43, 0x00, 0x00, 0x00)
		TESTFR = a2b_hex("680443000000")
		s.sendall(TESTFR)
		# -- receive TESTFR answer
		response = s.recv(BUFSIZE)
		print len(response)
		
		print "testfr sent / recv:%s / %s" %(b2a_hex(TESTFR), b2a_hex(response))
		to_return["testfr_sent_recv"] = b2a_hex(TESTFR) + '/' + b2a_hex(response)
		#-- send STARTDT command
		#local STARTDT = string.char(0x68, 0x04, 0x07, 0x00, 0x00, 0x00)
		STARTDT = a2b_hex("680407000000")
		s.sendall(STARTDT)
		#-- receive STARTDT answer
		response = s.recv(BUFSIZE)
		print len(response)	
		print "startdt sent / recv: %s / %s" %(b2a_hex(STARTDT), b2a_hex(response))
		to_return["startdt_sent_recv"] = b2a_hex(STARTDT) + '/' + b2a_hex(response)
		asdu_address = 0
		if len(response) == 22:
			(asdu_address,) = struct.unpack('<H', response[16:18])
		else:
			#-- send C_IC_NA_1 command
				#local C_IC_NA_1_broadcast = string.char(0x68, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x64, 0x01, 0x06, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x14)
				#status = socket:send( C_IC_NA_1_broadcast )
			C_IC_NA_1_broadcast = a2b_hex("680e0000000064010600ffff00000014")
			s.sendall(C_IC_NA_1_broadcast)			
			#-- receive C_IC_NA_1 answer
			response = s.recv(BUFSIZE)
			#table.insert(output, string.format("c_ic_na_1 sent / recv: %s / %s", stdnse.tohex(C_IC_NA_1_broadcast), stdnse.tohex(recv)))
			print "c_ic_na_1 sent / recv: %s / %s" %(b2a_hex(C_IC_NA_1_broadcast), b2a_hex(response))
			to_return["c_ic_na_1_sent_recv"] = b2a_hex(C_IC_NA_1_broadcast) + '/' + b2a_hex(response)
			if len(response) == 16:
				(asdu_address,) = struct.unpack('<H', response[10:12])
		if asdu_address:
			to_return["ASDU_address"] = asdu_address
	except Exception,e:
		print 'iec-identify get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	
	print to_return
	return to_return
