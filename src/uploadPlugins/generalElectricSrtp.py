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


#if __name__ == '__main__':
def scan(ip,port = 18245):
	string = "00"*56
	#print string
	#print len(string)
	
	packet_handshake = a2b_hex("00"*56)
	
	
	
	to_return={}
	
	
	#ip = "178.255.173.64"

	#address = ("", 0)
	
	TargetAddr = (ip, port)
	try:
		#TargetAddr = ("117.141.104.219", port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(TargetAddr)
		s.sendall(packet_handshake)
		response = s.recv(BUFSIZE)
		
		if len(response) == 56 and b2a_hex(response[8]) == '0f':
			to_return['ReplyMessage'] = response
			print to_return
	except Exception,e:
		print 'general-electric get error', str(e)
		to_return.clear()
	#else:
		#if to_return:	#not null
			#to_return["IP"] = ip
			#to_return["Port"] = port
			#to_return["TransportProtocol"] = "TCP"
	return to_return
