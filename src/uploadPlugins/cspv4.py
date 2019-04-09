#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#
#
'''
This script is used to send a CSPV4 packet to a remote device that has TCP 2222 open. This is a port used via CIP
and used by CSPV4 on AB PLC5 systems. This will determine the Session ID of the remote device to verify it as a CSPV4
compliant device.  CSPV4 or AB/Ethernet is used by Allen Bradley inside of its software products such as RSLinx to 
communicate to the PLCs. This will help ideitify some Allen Bradley PLCs that do not communicate via Ethernet/IP. 
Example: PLC5, SLC 500
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
def scan(ip,port=2222):

   init_coms = a2b_hex("01010000000000000000000000040005000000000000000000000000")
   
   to_return={}
   
   #address = ("", 0)
   try:
      TargetAddr = (ip, port)
      #TargetAddr = ("117.141.104.219", port)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      #s.bind(address)
      s.connect(TargetAddr)
      #response = send_receive(s, COTP)
      s.sendall(init_coms)
      
      response = s.recv(BUFSIZE)
      print len(response)
      
      first_check = b2a_hex(response[0])
      if first_check == '02':
         to_return['SessionID'] = int(b2a_hex(response[4:8][::-1]),16) #这里数据采用的是小端字节序，因此需要将解析的16进制字节进行逆序，采用[::-1]

   except Exception,e:
      print 'cspv4-info get error', str(e)
      #to_return["error"] = str(e)
      to_return.clear()

   return to_return
   
