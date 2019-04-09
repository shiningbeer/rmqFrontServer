#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
'''
The initial response is parsed to determine if host is a CoDeSys device. 
'''

import socket
import sys,os
import threading
import time
import string
import struct
from binascii import *

BUFSIZE = 10240	


#def dataSwitch(data):
	#str1 = ''
	#str2 = ''
	#while data:
		#str1 = data[0:2]
		#s = int(str1,16)
		#str2 += struct.pack('B',s)
		#data = data[2:]
	#return str2
def get_string(data):
	string = ""
	for c in data:
		if c == '\x00':
			break
		string += c	
	return string

#if __name__ == '__main__':
def scan(ip,port=1200):
	#lile_query = dataSwitch("bbbb0100000001")
	#bige_query = dataSwitch("bbbb0100000101")
	lile_query = a2b_hex("bbbb0100000001")
	bige_query = a2b_hex("bbbb0100000101")
	
	#to_return={}
	#to_return["IP"] = ip
	#to_return["Port"] = port
	#to_return["TransportProtocol"] = "TCP"
	
	#address = ("", 0)

	TargetAddr = (ip, port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#s.settimeout(15)	#设置timeout值低一点，以防没有响应时等待时间长
		s.connect(TargetAddr)
		s.sendall(lile_query)	#send little endian query
		
		response = s.recv(BUFSIZE)	#recieve response
		if len(response) == 0:	#if there was no response
			s.sendall(bige_query)	#send big endian query
			response = s.recv(BUFSIZE)	#recieve response
			
		print len(response)
		codesys_check = b2a_hex(response[0])
		if codesys_check != 'bb':
			s.close()
		
		#os_name = response[64:96]
		#os_type = response[96:128]
		#product_type = response[128:]
		to_return["OSName"] = get_string(response[64:96]) + ' ' + get_string(response[96:128])
		#to_return["os_type"] = 
		to_return["ProductType"] = get_string(response[128:])
		#print os_name,os_type,product_type
		print to_return
	except Exception,e:
		print 'codesys-v2 get error', str(e)
		to_return.clear()
	return to_return
	
