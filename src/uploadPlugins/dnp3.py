#!/usr/bin/ python
# -*- coding: utf-8 -*-
#
#shodan dork:"Source address:" "Control code:" port:"20000"
#
'''
This script will send a command to query through the first 100 addresses of 
DNP3 to see if a valid response is given. If a valid response is given it will
then parse the results based on function ID and other data. 
'''

import socket
import sys,os
import threading
import time
import string
import struct,copy
from binascii import *

BUFSIZE = 10240	#缓冲区大小10k

function_id = {
   0: "ACK",
   1: "NACK",
   11: "Link Status",
   15: "User Data"
}

alt_function_id = {
   0: "RESET Link",
   1: "Reset User Process",
   2: "TEST link",
   3: "User Data",
   4: "User Data",
   9: "Request Link Status"
}
first100 = a2b_hex("056405C900000000364C056405C901000000DE8E056405C" + 
    "9020000009F84056405C9030000007746056405C9040000" +
    "001D90056405C905000000F552056405C906000000B4580" + 
    "56405C9070000005C9A056405C90800000019B9056405C9" + 
    "09000000F17B056405C90A000000B071056405C90B00000" + 
    "058B3056405C90C0000003265056405C90D000000DAA705" +
    "6405C90E0000009BAD056405C90F000000736F056405C91" +
    "000000011EB056405C911000000F929056405C912000000" + 
    "B823056405C91300000050E1056405C9140000003A37056" +
    "405C915000000D2F5056405C91600000093FF056405C917" +
    "0000007B3D056405C9180000003E1E056405C919000000D" +
    "6DC056405C91A00000097D6056405C91B0000007F140564" +
    "05C91C00000015C2056405C91D000000FD00056405C91E00" +
    "0000BC0A056405C91F00000054C8056405C920000000014" +
    "F056405C921000000E98D056405C922000000A887056405" +
    "C9230000004045056405C9240000002A93056405C925000" +
    "000C251056405C926000000835B056405C9270000006B99" +
    "056405C9280000002EBA056405C929000000C678056405C" +
    "92A0000008772056405C92B0000006FB0056405C92C0000" +
    "000566056405C92D000000EDA4056405C92E000000ACAE0" +
    "56405C92F000000446C056405C93000000026E8056405C9" +
    "31000000CE2A056405C9320000008F20056405C93300000" +
    "067E2056405C9340000000D34056405C935000000E5F605" +
    "6405C936000000A4FC056405C9370000004C3E056405C93" +
    "8000000091D056405C939000000E1DF056405C93A000000" +
    "A0D5056405C93B0000004817056405C93C00000022C1056" +
    "05C93D000000CA03056405C93E0000008B09056405C93F0" +
    "0000063CB056405C940000000584A056405C941000000B0" +
    "88056405C942000000F182056405C943000000194005640" +
    "5C9440000007396056405C9450000009B54056405C94600" +
    "0000DA5E056405C947000000329C056405C94800000077B" +
    "F056405C9490000009F7D056405C94A000000DE77056405" +
    "C94B00000036B5056405C94C0000005C63056405C94D000" +
    "000B4A1056405C94E000000F5AB056405C94F0000001D69" +
    "056405C9500000007FED056405C951000000972F056405C" + 
    "952000000D625056405C9530000003EE7056405C9540000" +
    "005431056405C955000000BCF3056405C956000000FDF90" +
    "56405C957000000153B056405C9580000005018056405C9" +
    "59000000B8DA056405C95A000000F9D0056405C95B00000" +
    "01112056405C95C0000007BC4056405C95D000000930605" +
    "6405C95E000000D20C056405C95F0000003ACE056405C96" +
    "00000006F49056405C961000000878B056405C962000000" +
    "C681056405C9630000002E43056405C96400000044950")

def encode(s):
   return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
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
def scan(ip,port=20000):
   to_return={}
   
   #ip = '47.100.81.233'
   #address = ("", 0)
   
   #TargetAddr = ("77.88.110.252", port)
   #TargetAddr = ("166.247.131.139", port)
   #TargetAddr = ("216.197.184.153", port)
   TargetAddr = (ip, port)
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
      #s.bind(address)
      s.connect(TargetAddr)
      
      #response = send_receive(s, COTP)
      s.sendall(first100)
      response = s.recv(BUFSIZE)
      print len(response)
      byte1 = b2a_hex(response[0])
      byte2 = b2a_hex(response[1])
      
      output = {}
      if byte1 == '05' and byte2 == '64':
         dstadd = int(b2a_hex(response[4:6][::-1]),16)   #小端字节序，需要进行逆序
         print 'dstadd', dstadd
         srceadd = int(b2a_hex(response[6:8][::-1]),16)
         print 'srceadd', srceadd
         
         ctrl = '{0:b}'.format(ord(response[3]))   #将1个字节转为二进制流
         print 'ctrl', encode(ctrl)
         print 'len', len(ctrl)
         
         output["Source_Address"] = srceadd
         output["Destination_Address"] = dstadd
         output["Control"] = funct_lookup(ctrl)
         print output
      if output:
         #to_return["dnp3-info"] = copy.deepcopy(output)
         to_return.update(output)
         output.clear()
   except Exception,e:
      print 'dnp3-info error', str(e)
      #to_return["error"] = str(e)
      to_return.clear()

   return to_return

