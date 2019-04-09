#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
Tridium Niagara Fox is a protocol used within Building Automation Systems. Based
off Billy Rios and Terry McCorkle's work this Nmap NSE will collect information
from A Tridium Niagara system. The information is collected via TCP/1911, 
the default Tridium Niagara Fox Port.
'''

import socket
import sys,os
import threading
import time
import string
import struct
from binascii import *

BUFSIZE = 10240	#缓冲区大小10k

def funct_lookup(str_id):
	#这里string.byte是取对应字符串的内部编码，也就是ascii码
	print str_id
	funct_id = ""
	num = 0
	if len(str_id) < 5:
		print '<5'
		num = int(str_id, 2)
		if function_id.has_key(num):
			funct_id = function_id[num]
		else:
			funct_id = "Unknown Function ID"

	else:
		str_id = '{:0>8b}'.format(int(str_id,2))  #如果字符长度大于4位，在前面补0
		first_value = ord(str_id[1]) % 16  #取ascii码
		print 'first_value', first_value
		second_value = int(str(ord(str_id[4]) % 16) + str(ord(str_id[5]) % 16) + str(ord(str_id[6]) % 16) + str(ord(str_id[7]) % 16), 2)
		#int(str_id[4:7], 2)
		if first_value == 0:
			if function_id.has_key(second_value):
				funct_id = function_id[second_value]
			else:
				funct_id = "Unknown Function ID"
		elif alt_function_id.has_key(second_value):
			funct_id = alt_function_id[second_value]
		else:
			funct_id = "Unknown Function ID"
		num = second_value
	result = "%s (%d)" %(funct_id, num)
	return result
#if __name__ == '__main__':
def scan(ip,port = 1911):
	orig_query = a2b_hex("666f7820612031202d3120666f782068656c6c6f0a7b0a" +
	"666f782e76657273696f6e3d733a312e300a69643d693a310a686f73744e" +
	"616d653d733a7870766d2d306f6d64633031786d790a686f737441646472" +
	"6573733d733a3139322e3136382e312e3132350a6170702e6e616d653d73" +
	"3a576f726b62656e63680a6170702e76657273696f6e3d733a332e372e34" + 
	"340a766d2e6e616d653d733a4a61766120486f7453706f7428544d292053" +
	"657276657220564d0a766d2e76657273696f6e3d733a32302e342d623032" +
	"0a6f732e6e616d653d733a57696e646f77732058500a6f732e7665727369" +
	"6f6e3d733a352e310a6c616e673d733a656e0a74696d655a6f6e653d733a" +
	"416d65726963612f4c6f735f416e67656c65733b2d32383830303030303b" + 
	"333630303030303b30323a30303a30302e3030302c77616c6c2c6d617263" + 
	"682c382c6f6e206f722061667465722c73756e6461792c756e646566696e" +
	"65643b30323a30303a30302e3030302c77616c6c2c6e6f76656d6265722c" +
	"312c6f6e206f722061667465722c73756e6461792c756e646566696e6564" +
	"0a686f737449643d733a57696e2d393943422d443439442d353434322d30" +
	"3742420a766d557569643d733a38623533306263382d373663352d343133" +
	"392d613265612d3066616264333934643330350a6272616e6449643d733a" +
	"76796b6f6e0a7d3b3b0a")
	
	
	
	to_return={}
	#address = ("", 0)

	TargetAddr = (ip, port)
	#TargetAddr = ("117.141.104.219", port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#s.bind(address)
		s.connect(TargetAddr)
		#-- send the original query to see if it is a valid Niagara Fox Device
		s.sendall(orig_query)
		# -- receive response
		response = s.recv(BUFSIZE)
		print len(response)
		if len(response) == 0:	#if there was no response
			#没有响应
			print 'no response'
		output = {}
		print response
		if 'fox' in response:
			to_return['foxInfo'] = response
	except Exception,e:
		print 'fox-info get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	#else:
		#if to_return:	#not null
			#to_return["IP"] = ip
			#to_return["Port"] = port
			#to_return["TransportProtocol"] = "TCP"
	return to_return
