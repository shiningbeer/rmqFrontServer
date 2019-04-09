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
def scan(ip,port = 20547):

	req_info = a2b_hex("cc01000b4002000047ee")

	
	
	to_return={}
	#to_return["IP"] = ip
	#to_return["Port"] = port
	#to_return["TransportProtocol"] = "TCP"
	
	TargetAddr = (ip, port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
		s.connect(TargetAddr)
	
		s.sendall(req_info)
	
		response = s.recv(BUFSIZE)
		print len(response)
	
		check1 = b2a_hex(response[0])
		if check1 == 'cc':
			pos, to_return["Ladder_Logic_Runtime"] = getZeroTerminatedString(response, 12)
			pos, to_return["PLC_Type"] = getZeroTerminatedString(response, 44)
			pos, to_return["Project_Name"] = getZeroTerminatedString(response, 77)
			pos, to_return["Boot_Project"] = getZeroTerminatedString(response, pos)
			pos, to_return["Project_Source_Code"] = getZeroTerminatedString(response, pos)
			
	except Exception,e:
		print 'proconos-info get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	#print to_return
	return to_return
