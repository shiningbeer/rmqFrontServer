#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
discovery Mitsubishi Electric Q Series PLC 
	GET CPUINFO
'''

import socket
import sys,os
import threading
import time
import string
import struct
from binascii import *

BUFSIZE = 10240	#缓冲区大小10k

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
def scan(ip,port = 5007):
	getcpuinfopack = a2b_hex("57000000001111070000ffff030000fe03000014001c080a080000000000000004" + "0101" + "010000000001")
	
	
	to_return={}
	#to_return["IP"] = ip
	#to_return["Port"] = port
	#to_return["TransportProtocol"] = "TCP"
	#ip = "82.219.226.234"
	#ip = "211.43.161.45"


	TargetAddr = (ip, port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(TargetAddr)
		s.sendall(getcpuinfopack)
		response = s.recv(BUFSIZE)
		print len(response)
		
		if len(response) > 0:
			(pack_head, ) = struct.unpack("B", response[0])
			if pack_head == int('0xd7', 16):
				#local mel, cpuinfo = bin.unpack("z", response, 42 + offset)
				pos, cpuinfo = getZeroTerminatedString(response, 41)
				to_return['CPUINFO'] = cpuinfo
	
	except Exception,e:
		print 'melsecq-discover get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	#print to_return
	return to_return	

