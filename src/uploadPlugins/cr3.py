#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
Fingerprints Red Lion HMI devices
Perform discovery using Red Lion Crimson V3 Protocol
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
def scan(ip,port=789):
	probe_manufacturer = a2b_hex("0004012b1b00")
	
	port = 789
	to_return={}	

	try:
		TargetAddr = (ip, port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		s.connect(TargetAddr)
		
		s.sendall(probe_manufacturer)
		
		response = s.recv(BUFSIZE)
		print len(response)
		if len(response) > 2:
			#resp_string = "\nManufacturer:" + 
			if "Red Lion" in response[6:-1]:
				to_return['Manufacturer'] = response[6:-1]
				
				probe_manufacturer2 = a2b_hex("0004012a1a00")
				s.sendall(probe_manufacturer2)
				
				response2 = s.recv(BUFSIZE)
				print len(response2)
				if len(response2) > 2:
					#resp_string = "\nManufacturer:" + 
					to_return['Model'] = response2[6:-1]
	except Exception,e:
		print 'cr3-fingerprint get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	#else:
		#if to_return:	#not null
			#to_return["IP"] = ip
			##to_return["Port"] = port
			##to_return["TransportProtocol"] = "TCP"	
	return to_return
