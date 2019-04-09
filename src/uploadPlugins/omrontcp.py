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

memcard = {
    "0" : "No Memory Card",
    "1" : "SPRAM",
    "2" : "EPROM",
    "3" : "EEPROM"
}

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
def scan(ip,port = 9600):
		
	req_addr = a2b_hex("46494e530000000c000000000000000000000000")
	
	controller_data_read = a2b_hex("46494e5300000015000000020000000080000200")
	controller_data_read2 = a2b_hex("000000ef050501")
	
	#ip = "195.228.211.245"
	#ip = "5.144.145.198"
	
	#address = ("", 0)
	
	to_return={}
	
	TargetAddr = (ip, port)
	#TargetAddr = ("117.141.104.219", port)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
		#s.bind(address)
		s.connect(TargetAddr)
		#-- send the original query to see if it is a valid Niagara Fox Device
		s.sendall(req_addr)
	
	
		# -- receive response
		response = s.recv(BUFSIZE)
		print len(response)
		if len(response) == 0:	#if there was no response
			#没有响应
			print 'no response'
		header = b2a_hex(response[0])
		if header == '46':
			address, = struct.unpack('B', response[23])
			print type(address), address
			#local controller_data = bin.pack("HCHC", controller_data_read, address, controller_data_read2, 0x00)
			fmt = "%dsB%dsB" %(len(controller_data_read), len(controller_data_read2))
			controller_data = struct.pack(fmt,controller_data_read, address, controller_data_read2, 0)
			#controller_data = struct.pack("20sB", controller_data_read, address)
			#print controller_data
			s.sendall(controller_data)
			response = s.recv(BUFSIZE)
			if len(response) == 0:	#if there was no response
				#没有响应
				print 'no response'
			else:
				response_code, = struct.unpack("<H", response[28:30])
				if response_code == 2081:
					to_return["ResponseCode"] = "Data cannot be changed (0x2108)"
				elif(response_code == 290):
					to_return["ResponseCode"] = "The mode is wrong (executing) (0x2201)"
				elif(response_code == 0):
					to_return["ResponseCode"] = "Normal completion (0x0000)"
					
					pos, to_return["Controller_Model"] = getZeroTerminatedString(response, 30)
					pos, to_return["Controller_Version"] = getZeroTerminatedString(response, 50)
					pos, to_return["For_System_Use"] = getZeroTerminatedString(response, 70)
					to_return["Program_Area_Size"], = struct.unpack(">H",response[110:112])
					to_return["IOM_size"], = struct.unpack("B",response[112])
					to_return["No.DM_Words"], = struct.unpack(">H",response[113:115])
					to_return["Timer/Counter"], = struct.unpack("B",response[115])
					to_return["Expansion_DM_Size"], = struct.unpack("B",response[116])
					to_return["No._of_steps/transitions"], = struct.unpack(">H",response[117:119])
					
					Kind_of_Memory_Card = ""
					mem_card_type, = struct.unpack("B",response[119])
					if memcard.has_key(str(mem_card_type)):
						Kind_of_Memory_Card = memcard[str(mem_card_type)]
					else:
						Kind_of_Memory_Card = "Unknown Memory Card Type"
					to_return["Kind_of_Memory_Card"] = Kind_of_Memory_Card
					
					to_return["Memory_Card_Size"], = struct.unpack(">H",response[120:122])
	
	except Exception,e:
		print 'omrontcp get error', str(e)
		#to_return["error"] = str(e)
		to_return.clear()
	#print to_return
	#else:
		#if to_return:	#not null
			#to_return["IP"] = ip
			#to_return["Port"] = port
			#to_return["TransportProtocol"] = "TCP"
	return to_return

