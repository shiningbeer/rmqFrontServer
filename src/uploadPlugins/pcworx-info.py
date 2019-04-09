#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
This script will query and parse pcworx protocol to a remote PLC. 
The script will send a initial request packets and once a response is received,
it validates that it was a proper response to the command that was sent, and then 
will parse out the data. PCWorx is a protocol and Program by Phoenix Contact. 
'''

import socket
import sys,os
import threading
import time
import string
import struct
from binascii import *

BUFSIZE = 10240

#def getZeroTerminatedString(res):
	#data = ""
	#for i in res:
		#if b2a_hex(i) != '00':
			#data += i
		#else:
			#break
	#return data
def getZeroTerminatedString(response,pos):
	data = ""
	for i in range(pos,len(response)) :
#	in response[pos:]:
		if b2a_hex(response[i]) != '00':
		#b2a_hex(i) != '00':
			data += response[i]
		else:
			end_pos = i + 1
			break
	return end_pos, data
#if __name__ == '__main__':
def scan(ip,port = 1962):

	init_coms = a2b_hex("0101001a0000000078800003000c494245544830314e305f4d00")
	
	
	
	to_return={}

	#address = ("", 0)
	TargetAddr = (ip, port)
	#TargetAddr = ("117.141.104.219", port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(TargetAddr)
		s.sendall(init_coms)
		response = s.recv(BUFSIZE)
		print len(response)
	
		sid = ord(response[17])
		#address, = struct.unpack('B', response[17])
		#print type(address), address
		
		print sid,type(sid)
		init_comms2 = struct.pack("11sB10s",a2b_hex("0105001600010000788000"), sid, a2b_hex("00000006000402950000"))
		print repr(init_comms2)
		
		s.sendall(init_comms2)
		response = s.recv(BUFSIZE)
		print len(response)
		
		req_info = struct.pack("11sB2s",a2b_hex("0106000e00020000000000"), sid, a2b_hex("0400"))
		#local req_info = bin.pack("HCH","0106000e00020000000000",sid,"0400")
		
		s.sendall(req_info)
		response = s.recv(BUFSIZE)
		print len(response)
		
		check1 = b2a_hex(response[0])
		if check1 == '81':
			pos, to_return["PLC_Type"] = getZeroTerminatedString(response, 30)
			pos, to_return["Model_Number"] = getZeroTerminatedString(response, 152)
			pos, to_return["Firmware_Version"] = getZeroTerminatedString(response, 66)
			pos, to_return["Firmware_Date"] = getZeroTerminatedString(response, 79)
			pos, to_return["Firmware_Time"] = getZeroTerminatedString(response, 91)
	except Exception,e:
		print 'pcworx-info get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	#print to_return
	#else:
		#if to_return:	#not null
			#to_return["IP"] = ip
			#to_return["Port"] = port
			#to_return["TransportProtocol"] = "TCP"
	return to_return