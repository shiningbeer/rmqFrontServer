#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#
"""
File: modbus.py
Develop Code Time: 1 day
Desc:
整合modicon-info.nse和modbus-discover.nse两个插件，根据响应信息判断是否获取下一步信息
Device Identification
流程：先获取设备标识符（Device Identification），根据这个来进行判断下一步操作
如果获取该信息出错，就获取slave Info信息
如果其中包含Schneider，就通过modicon插件
"""

from struct import pack,unpack
import socket

import string
from binascii import *
import copy,sys

class ModbusError(Exception):
    _errors = {
        0:      'No reply',
        # Modbus errors
        1:      'ILLEGAL FUNCTION',
        2:      'ILLEGAL DATA ADDRESS',
        3:      'ILLEGAL DATA VALUE',
        4:      'SLAVE DEVICE FAILURE',
        5:      'ACKNOWLEDGE',
        6:      'SLAVE DEVICE BUSY',
        8:      'MEMORY PARITY ERROR',
        0x0A:   'GATEWAY PATH UNAVAILABLE',
        0x0B:   'GATEWAY TARGET DEVICE FAILED TO RESPOND'
    }
    def __init__(self,  code):
        self.code = code
        self.message = ModbusError._errors[code] if ModbusError._errors.has_key(code) else 'Unknown Error'
    def __str__(self):
        return "[Error][Modbus][%d] %s" % (self.code, self.message)


class ModbusPacket:
    def __init__(self, transactionId=0, unitId=0, functionId=0, data=''):
        self.transactionId = transactionId
        self.unitId = unitId
        self.functionId = functionId
        self.data = data

    def pack(self):
        return pack('!HHHBB',
            self.transactionId,          # transaction id
            0,                           # protocol identifier (reserved 0)
            len(self.data)+2,            # remaining length
            self.unitId,                 # unit id
            self.functionId              # function id
        ) + self.data                    # data

    def unpack(self,packet):
        if len(packet)<8:
            print 'Response too short'
            return -1
        self.transactionId, self.protocolId, length, self.unitId, self.functionId = unpack('!HHHBB',packet[:8])
        if len(packet) < 6+length:
            print 'Response too short'
            return -1   #error

        #self.data = packet[8:]
        self.data = packet
        return self

class Modbus:
    def __init__(self, sock, ip, port=502):
        self.sock = sock
        self.ip = ip
        self.port = port
        #self.uid = uid
    def Request(self, transactionId, functionId, data, uid):
        #sock = self.sock
        self.sock.send(ModbusPacket(transactionId, uid, functionId, data).pack())
        reply = self.sock.recv(1024)

        if not reply:
            result = ModbusError(0).message
            return -1,result

        response = ModbusPacket().unpack(reply)
        if response == -1:
            return -1, '(error)'
        if response.unitId != uid:
            print 'Unexpected unit ID or incorrect packet'  #跳出执行
            return -1, '(error)'    #-1代表出错

        if response.functionId != functionId:
            result = ModbusError(ord(response.data[8])).message
            return -1, result    #0,代表是modbus相关错误
        #sock.close()
        result = response.data
        return 1, result

    def DeviceInfo(self, uid):
        status, res = self.Request(0x00, 0x2b, '\x0e\x01\00', uid)
        if status == -1:
            return res
        #elif status == 0:
            #return res
        elif status == 1 and len(res) > 5:
            objectsCount = ord(res[5+8])
            data = res[6+8:]
            info = ''
            for i in range(0, objectsCount):
                info += data[2:2+ord(data[1])]
                info += ' '
                data = data[2+ord(data[1]):]
            return info
        else:
        #    raise ModbusProtocolError('Packet format (reply for device info) wrong', res)
            return -1
    def SlaveID(self, uid):
        status,res = self.Request(0x00, 0x11, '', uid)
        data = ''
        if status == -1:
            print 'error, end!!!!'
            print res
            data = res
        else:
        #elif len(res)>3:
            for i in res:
                if ord(i) > 31 and ord(i) < 128:
                    data += i
            if not data:    #
                data = '0x' + b2a_hex(res)
            print data
        return data
    def CpuModuleInfo(self,uid):
        
        status,res = self.Request(0x01, 0x5a, '\x00\x02', uid)
        #status,res = self.Request(0x11)
        data = ''
        if status == -1:
            print 'error, end!!!!'
            print res
            data = res
        else:
            size = ord(res[24+8])
            data = res[25+8:25+8+size]
            #for i in res:
                #if ord(i) > 31 and ord(i) < 128:
                    #data += i
            print data
        return data
    def MemoryCardInfo(self, uid):
        
        status,res = self.Request(0x01bf, 0x5a, '\x00\x06\x06', uid)
        #status,res = self.Request(0x11)
        data = ''
        if status == -1:
            print 'error, end!!!!'
            print res
            data = res
        else:
            size = ord(res[8+8])  #返回的data去除了前面8个字节
            data = res[9+8:9+8+size]
            #for i in res:
                #if ord(i) > 31 and ord(i) < 128:
                    #data += i
            print data
        return data
    def ProjectInfomation(self, uid):
        status,res = self.Request(0x0004, 0x5a, '\x00\x03\x00', uid)
        #status,res = self.Request(0x11)
        data = ''
        project_name = ''
        if status == -1:
            print 'error, end!!!!'
            print res
            data = res
        else:
            for i in res[41+8:]:
                if b2a_hex(i) != '00':
                    project_name += i
            #-- unpack the seconds
            project_sec = ord(res[29+8])
            #-- unpack the min
            project_min = ord(res[30+8])
            #-- unpack the hour
            project_hour = ord(res[31+8])
            #-- unpack the day
            project_day = ord(res[32+8])
            #-- unpack the month
            project_month = ord(res[33+8])
            (project_year,) = unpack("<H", res[34+8:36+8])
           # project_year = res[34:38]
            print type(project_year)
            
            #-- The next 3 are for the revision number
            project_rev_1 = ord(res[36+8])
            project_rev_2 = ord(res[37+8])
            project_rev_3 = ord(res[38+8])
            output["Project_Revision"] = str(project_rev_3) + "." + str(project_rev_2) + "." + str(project_rev_1)
            output["ProjectLastModified"] = str(project_month) + "/" + str(project_day) + "/" + str(project_year) + \
                " " + str(project_hour) + ":" + str(project_min) + ":" + str(project_sec)
            
            status,res = self.Request(0x000f, 0x5a, a2b_hex('002000140064000000f600'), uid)
            if status == -1:
                print 'error, end!!!!'
                print res
                data = res
            else:
                project_info = ""
                size = ord(res[5])
                print len(res)
                for i in res[179:179+size+6]:
                    if b2a_hex(i) == '00':
                        project_info += ' '
                    else:
                        project_info += i
                print project_info
            
            project_fn = ""
            status,res = self.Request(0x0010, 0x5a, a2b_hex('00200014005a010000f600'), uid)
            if status == -1:
                print 'error, end!!!!'
                print res
                data = res
            else:
                for i in res[13:]:
                    if b2a_hex(i) != '00':
                        project_fn += i
            output["ProjectInformation"] = project_name + "-" + project_info + project_fn
            print output["ProjectInformation"]
        return output
    
        
#if __name__ == '__main__':
def scan(ip,port = 502):
    
    to_return = {}
    

    #ip = "188.226.166.15"
    
    #ip = "81.225.234.68"
    #ip = "142.54.210.176"
    #ip = "140.114.206.160"
    #ip = "77.211.16.196"
    #ip = "84.100.6.121"
    #TargetAddr = ("81.225.234.68", port)
    #uids = [0,255]
    
    #ip = '84.100.6.121'
    #ip = '120.157.85.57'
    #ip = '173.181.212.179'
    uids = [0,1,255]    #这里只取有限个uid

    output = {}
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        try:
            sock.connect((ip, port))
        except Exception, e:
            print str(e)
            to_return['error'] = str(e)
            sys.exit(0)
        con = Modbus(sock, ip, port)
        for uid in uids:
           
            deviceInfo = ''
            #先获取DeviceIdentification
            try:
                deviceInfo = con.DeviceInfo(uid)
            except Exception,e:
                #deviceInfo = str(e)
                print 'get deviceInfo error:', str(e)
                continue
            else:
                if not deviceInfo:    #deviceInfo为空，说明没有数据，出错
                    continue
                else:
                    output['DeviceIdentification'] = deviceInfo
            if 'Schneider' not in deviceInfo:   #如果deviceinfo出错或者不是schneider，就获取slaveid并继续运行
                SlaveIDdata = ''
                #get slave id
                try:
                    SlaveIDdata = con.SlaveID(uid)
                except Exception,e:
                    #SlaveIDdata = str(e)
                    print 'get slave id error:', str(e)
                finally:
                    output['SlaveIDdata'] = SlaveIDdata
                    #说明deviceInfo中有正常数据且不是schneider，就获取slaveid后退出
                #print str(ModbusError._errors)
                #if '(error)' not in deviceInfo and '(error)' not in SlaveIDdata and deviceInfo not in str(ModbusError._errors) and SlaveIDdata not in str(ModbusError._errors):
                if ('(error)' not in (deviceInfo or SlaveIDdata) ) and ('No reply' not in(deviceInfo or SlaveIDdata)) :
                #ModbusError(0).message not in deviceInfo:
                    #print deviceInfo
                    to_return['UnitID_' + str(uid)] = copy.deepcopy(output)
                    break
                else:
                    continue                
            else:
                #get schneider相关信息
                try:
                    #----CPU Module
                    CpuModuleInfo = ''
                    CpuModuleInfo = con.CpuModuleInfo(uid)
                    output['CpuModule'] = CpuModuleInfo
                    
                    #----Memory Card
                    MemoryCardInfo = ''
                    MemoryCardInfo = con.MemoryCardInfo(uid)
                    output['MemoryCard'] = MemoryCardInfo
                    
                    #----project infomation
                    ProjectInfomation = ''
                    ProjectInfomation = con.ProjectInfomation(uid)
                    print ProjectInfomation
                    output.update(ProjectInfomation)
                except Exception,e:
                    print 'get schneider infomation error'
                    
                finally:
                    to_return['UnitID_' + str(uid)] = copy.deepcopy(output)
                    break      
            if output:
                to_return['UnitID_' + str(uid)] = copy.deepcopy(output)
                output.clear()
            #to_return['UnitID_' + str(uid)] = copy.deepcopy(output)
            #output.clear()
        sock.close()
    except Exception,e:
        print 'modbus get error', str(e)
        #to_return["error"] = str(e)
        to_return.clear()

    return to_return
    
