#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
This script is used to send a srtp packet to a remote device that has TCP 18245 open. 
'''

import socket
import sys,os
import threading
import time
import string
import struct
from binascii import *

BUFSIZE = 10240
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
def scan(ip,port = 30718):
	L77FEH_RCR = a2b_hex("000000F4")
	L77FEH_INF = a2b_hex("000000F6")
	L77FEH_SETUP = a2b_hex("000000F8")
	
	
	
	to_return={}
	#to_return["IP"] = ip
	#to_return["Port"] = port
	#to_return["TransportProtocol"] = "TCP"
	
	#ip = "24.49.228.64"

	address = ("", 0)
	try:
		TargetAddr = (ip, port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
		s.connect(TargetAddr)
	
		#response = send_receive(s, COTP)
		s.sendall(L77FEH_RCR)
	
		response = s.recv(BUFSIZE)
		print len(response)
		if b2a_hex(response[0:4]) == '000000f5':
			pos,version = getZeroTerminatedString(response,16)
			to_return["version"] = version
		
		
		s.sendall(L77FEH_INF)
		response = s.recv(BUFSIZE)
		print len(response)
		if b2a_hex(response[0:4]) == '000000f7':
			#pos,version = getZeroTerminatedString(response[16:])
			devtype, = struct.unpack("3s", response[8:11])
			devmac, = struct.unpack("6s", response[24:30])
			#to_return["version"] = version
			to_return["Device_Type"] = devtype
			to_return["MAC_address"] = devmac
		
		s.sendall(L77FEH_SETUP)
		response = s.recv(BUFSIZE)
		print len(response)
		if b2a_hex(response[0:4]) == '000000f9':
			#pos,version = getZeroTerminatedString(response[16:])
			simplepass, = struct.unpack("4s", response[12:16])
			#to_return["version"] = version
			to_return["Password"] = simplepass
	except Exception,e:
		print 'lantronix-electric get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	return to_return
