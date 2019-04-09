#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
This Script is designed to query the I20100 command on Guardian AST Automatic Tank Gauge
products. This script sends a single query and parses the response. This response is the Tank Inventory 
of the ATG. Using --script-args command=I20200 you will be able to pull a diffrent report than the I20100.
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
def scan(ip):
	
	port = 10001
	command = "I20100"
	to_return={}
	
	#to_return["IP"] = ip
	#to_return["Port"] = port
	#to_return["TransportProtocol"] = "TCP"

	TargetAddr = (ip, port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(15)	#设置timeout值低一点，以防没有响应时等待时间长
		s.connect(TargetAddr)
		tank_command = "\x01" + command + "\n"
		s.sendall(tank_command)
		response = s.recv(1024)
		#print len(response)
		if len(response) == 0:
			print "len response is 0"
			return to_return
		first_byte = b2a_hex(response[0])
		inventory_output = ""
		if first_byte == '01' or first_byte == '0a':
			response2 = s.recv(1024)
			while len(response2):
				if b2a_hex(response2[-1]) == '03':	#检测结尾是否为ETX
					inventory_output += response2[:-1]
					break
				else:
					inventory_output += response2
					#print inventory_output
					response2 = s.recv(1024)
			#print inventory_output
		#s.settimeout(None)
		if inventory_output:	#not null
			to_return["inventory_output"] = inventory_output
	except Exception,e:
		print 'atg-info get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	
	return to_return

