# -*- coding: utf8 -*-


__author__ = '1212'

import struct
from ICSScanEngine import Utility
import Device
_logger = Utility.ThreadLog('Ice_104', 'Device.log')

class Ice_104Device(Device.TCPDevice):
    DEFAULT_PORTS = [2404,]
    PROTOCOL_NAME = 'IEC60870-5-104'

    def __init__(self, ip, port=DEFAULT_PORTS[0]):
        super(Ice_104Device, self).__init__(ip, port)
        self.vendor = '未知'
        self.type = "protocol"
        self.protocol = self.PROTOCOL_NAME
        self.message_len=''
        self.asdu_addr=''
        self.ctr_code=''
        self.message_type=''
        self.cause=''
        self.info=''
        self.limited=''

    def __str__(self):
        return '信息长度: %s \nASDU地址: %s \n控制字节: %s \n数据类型: %s \n帧限定词: %s \n传输原因: %s \n信息体: %s' % (
        self.message_len,
        self.asdu_addr,
        self.ctr_code,
        self.message_type,
        self.limited,
        self.cause,
        self.info
        )
    def get_identity(self):
        TESTFR='\x68\x04\x43\x00\x00\x00'      #/ 680483000000 #
        STARTDT='\x68\x04\x07\x00\x00\x00'     #/ 68040b000000
        C_IC_NA_1='\x68\x0e\x00\x00\x00\x00\x64\x01\x06\x00\xff\xff\x00\x00\x00\x14'# / 680e0000020064014700ffff00000014
        recv_data =self.request(TESTFR)
        if((recv_data[:1]=='\x68')and(recv_data[2:3]=='\x83')):
            test=str(struct.unpack('!%dB' %(ord(recv_data[1:2])+2),recv_data))        #test
            self.fingerprint='链路测试: %s \n'%test
            #self.fingerprint='链路测试: %s \n'%repr(recv_data)
            recv_data=self.request(STARTDT)
            if((recv_data[:1]=='\x68')and(recv_data[2:3]=='\x0b')):           #startand
                link=str(struct.unpack('!%dB' %(ord(recv_data[1:2])+2),recv_data[:6]))
                self.fingerprint+='传输启动: %s \n'%link
                recv_data=self.request(C_IC_NA_1)                           #请求数据
                #self.rcv_data=repr(recv_data)
                self.message_len ,= struct.unpack('!B',recv_data[1:2])
                #self.message_len = hex(self.message_len)
                self.ctr_code , = struct.unpack('!I',recv_data[2:6])           #控制字节
                #self.ctr_code = hex(self.ctr_code)
                self.message_type ,= struct.unpack('!B',recv_data[6:7])
                #self.message_type = hex(self.message_type)                     #数据类型
                self.limited ,= struct.unpack('!B',recv_data[7:8])             #侦限定词
                #self.limited = hex(self.limited)
                self.cause ,= struct.unpack('!H',recv_data[8:10])
                #self.cause= hex(self.cause)                                #数据原因
                self.asdu_addr ,= struct.unpack('!H',recv_data[10:12])
                #self.asdu_addr = hex(self.asdu_addr)                          #地址
                #self.info=repr(recv_data[12:])
                self.info=str(struct.unpack('!%dB' %(self.message_len-10),recv_data[12:2+self.message_len]))
                self.fingerprint+='信息长度: 0x%02x \nASDU地址: 0x%04x \n控制字节: 0x%08x \n数据类型: 0x%02x \n帧限定词: 0x%02x \n传输原因: 0x%04x \n信息体: %s'% (
                self.message_len,
                self.asdu_addr,
                self.ctr_code,
                self.message_type,
                self.limited,
                self.cause,
                self.info
                )
            return True
        else:
            _logger.warn('不能识别的应答数据[%s]' % repr(recv_data))
            return False
def scan(ip, port = 2404):
    """扫描104设备，成功则返回104对象，否则返回None"""
    device = Ice_104Device(ip, port)
    result = None

    for x in range(device.retry):
        try:
            if not device.connect():
                continue

            if device.get_identity():
                result = device
                break
        except:
            # _logger.error('%s - %s' % (ip, e))
            pass
    device.disconnect()
    return result

if __name__ == '__main__':
    #print scan('221.207.5.141')
    print scan('5.11.149.14')
