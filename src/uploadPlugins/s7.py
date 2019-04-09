#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#2016.8.24 修改程序中取响应的方法，之前的方法是截取一段响应，根据响应的ascii，取可以正常显示的ascii（也就是在32-126之间的）
#目前的方法是根据这段响应字符串，判断字符串的十六进制是否为00，如果为00就不再截取
#

import socket
import sys
import threading
import time
import string
import struct,copy
from binascii import *

BUFSIZE = 10240	#缓冲区大小10k

#orig_query = bin(int('810a001101040005010c0c023FFFFF194b',16)).replace('0b','')	# Hex to binary
str_send = '810a001101040005010c0c023FFFFF194b'
#print str_send

def send_receive(sock, query):
    try:
        sendstatus = sock.sendall(query)
        data = sock.recv(BUFSIZE)
        return data
    except Exception, e:
        print "failed", e
        return "Error Sending or Reading S7COMM"

def parse_response(response):
    value = b2a_hex(response[7])
    szl_id = b2a_hex(response[30])
    offset = 0
    output = {}
    if value == '32':
        #output['Module'] = a2b_hex(b2a_hex(response[42:63]))
        #output["Basic Hardware"] = a2b_hex(b2a_hex(response[72:92]))
       # int(b2a_hex(data[19:22]),16)
        
        output['Module'] = response[43:63]
        #delete the character, that the ascii is between 32 and 126
        for c in response[63:71]:
            #if 32 <= ord(c) <= 126:
                #output['Module'] += c
            if c == '\x00':
                break
            output['Module'] += c
            
        print output['Module']
        
        output["BasicHardware"] = response[71:91]
        for c in response[91:121]:
            #if 32 <= ord(c) <= 126:
                #output['BasicHardware'] += c
            #if b2a_hex(c) == '00': #取十六进制
            if c == '\x00':
                break
            output['BasicHardware'] += c
        
        output['Version'] = str(ord(response[122])) + '.' + str(ord(response[123])) + '.' + str(ord(response[124]))
        print output['Version']
        
        #string = struct.pack('BBB', ord(response[122]), ord(response[123]), ord(response[124]))
        string = struct.pack('3s', response[122:125])
        print string
        
        #print 'version', repr(response[122:125])
        #print ord(response[122]),ord(response[123]),ord(response[124])
        #output['Module'] = a2b_hex(int(response[42:62],16))
        
        return output
    else:
        return 0
def second_parse_response(response):
    offset = 0
    output = {}
    value = b2a_hex(response[7])
    szl_id = b2a_hex(response[30])
    if value == '32':
        if szl_id != '1c':
            offset = 4
        #output['System Name'] = response[39 + offset : 49 + offset]
        #parse system name
        output['SystemName'] = ''
        for c in response[39 + offset : 73 + offset]:
            #if 32 <= ord(c) <= 126:
                #output['SystemName'] += c
            #if b2a_hex(c) == '00': #取十六进制
            if c == '\x00':
                break
            output['SystemName'] += c
            
        print output['SystemName']        
        #parse module type
        output['ModuleType'] = ''
        for c in response[73 + offset : 107 + offset]:
            #if 32 <= ord(c) <= 126:
                #output['ModuleType'] += c
            
            #if b2a_hex(c) == '00': #取十六进制
            if c == '\x00':
                break
            output['ModuleType'] += c
        print output['ModuleType']
        #parse serial number
        output['SerialNumber'] = ''
        for c in response[175 + offset : 209 + offset]:
            #if 32 <= ord(c) <= 126:
                #output['SerialNumber'] += c
            #if b2a_hex(c) == '00':
                #break
            #if b2a_hex(c) == '00': #取十六进制
            if c == '\x00':
                break            
            output['SerialNumber'] += c
            
        print output['SerialNumber']
        
        #parse plant identification
        output['PlantIdentification'] = ''
        for c in response[107 + offset : 141 + offset]:
            #if 32 <= ord(c) <= 126:
                #output['PlantIdentification'] += c
            #if b2a_hex(c) == '00':
                #break
            #if b2a_hex(c) == '00': #取十六进制
            if c == '\x00':
                break            
            output['PlantIdentification'] += c            
            
        print output['PlantIdentification']
        #parse copyright
        output['Copyright'] = ''
        for c in response[141 + offset : 175 + offset]:
            #if 32 <= ord(c) <= 126:
                #output['Copyright'] += c
            #if b2a_hex(c) == '00':
                #break
            #if b2a_hex(c) == '00': #取十六进制
            if c == '\x00':
                break
            output['Copyright'] += c
            
        print output['Copyright']
    return output
        
def scan(ip,port = 102  ):        

    #portrule = shortport.port_or_service(47808, "bacnet", "udp")
    #if len(sys.argv) != 3:
        #_usage()
        #sys.exit(1)
    #IP = sys.argv[1]
    #port = sys.argv[2]
    #IP = '0.0.0.0'
    
    COTP = a2b_hex("0300001611e00000001400c1020100c2020" + "102" + "c0010a")
    alt_COTP = a2b_hex("0300001611e00000000500c1020100c2020" + "200" + "c0010a")
    ROSCTR_Setup = a2b_hex("0300001902f08032010000000000080000f0000001000101e0")
    Read_SZL = a2b_hex("0300002102f080320700000000000800080001120411440100ff09000400110001")
    first_SZL_Request = a2b_hex("0300002102f080320700000000000800080001120411440100ff09000400110001")
    second_SZL_Request = a2b_hex("0300002102f080320700000000000800080001120411440100ff090004001c0001")
    
    
    to_return={}
    #to_return["IP"] = ip
    #to_return["Port"] = port
    #to_return["TransportProtocol"] = "TCP"
    

    address = ("", 0)
    #TargetAddr = ("91.113.136.227", port)
    TargetAddr = (ip, port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #s.bind(address)
        s.connect(TargetAddr)
        
        #response = send_receive(s, COTP)
        s.sendall(COTP)
        response = s.recv(BUFSIZE)
        print len(response)
        CC_connect_confirm = b2a_hex(response[5])
        #if PDU type is not 0xd0, then not a successful COTP connection
        if CC_connect_confirm != 'd0':
            s.close()
            #create socket for communications
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(TargetAddr)
            
            sock.sendall(alt_COTP)
            response = sock.recv(BUFSIZE)
            CC_connect_confirm = b2a_hex(response[5])
            if CC_connect_confirm != 'd0':
                print "S7 INFO:: Could not negotiate COTP"
                #return 0
        
        # send and receive the ROSCTR Setup Packet
        s.sendall(ROSCTR_Setup)
        response = s.recv(BUFSIZE)
        protocol_id = b2a_hex(response[7])
        #if protocol ID is not 0x32 then return 0
            
        #send and receive the READ_SZL packet
        s.sendall(Read_SZL)
        response = s.recv(BUFSIZE)
        
        # send and receive the first SZL Request packet
        s.sendall(first_SZL_Request)
        response = s.recv(BUFSIZE)
        # parse the response for basic hardware information
        output = {}
        output1 = parse_response(response)
        # send and receive the second SZL Request packet
        s.sendall(second_SZL_Request)
        response = s.recv(BUFSIZE)
        # parse the response for more information
        output2 = second_parse_response(response)
        output = dict(output1, **output2)
          
        #print output
        if output:
            #to_return["dnp3-info"] = copy.deepcopy(output)
            to_return['data'] = copy.deepcopy(output)
            output.clear()
            to_return['IP'] = ip
        #to_return["output"] = output
    except Exception,e:
        print 's7-enumerate get error', str(e)
        to_return.clear()
    return to_return

    #while True:
        #pass
if __name__ == '__main__':
    ip = '37.247.92.40'
    dict_s7 = scan(ip)
    print dict_s7