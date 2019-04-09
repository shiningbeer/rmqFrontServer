# -*- coding: utf8 -*-


__author__ = '1212'

from struct import *
from random import randint
from optparse import OptionGroup

import struct
import socket
import string

import Device
import FingerprintDict
from ICSScanEngine import Utility

_logger = Utility.ThreadLog('S7', 'Device.log')

__FILTER = "".join([' '] + [' ' if chr(x) not in string.printable or chr(x) in string.whitespace else chr(x) for x in range(1,256)])
def StripUnprintable(msg):
    return msg.translate(__FILTER)

class TPKTPacket:
    """ TPKT packet. RFC 1006
    """
    def __init__(self, data=''):
        self.data = str(data)
    def pack(self):
        return pack('!BBH',
            3,                  # version
            0,                  # reserved
            len(self.data)+4    # packet size
        ) + str(self.data)
    def unpack(self,packet):
        try:
            header = unpack('!BBH', packet[:4])
        except struct.error as e:
            raise S7ProtocolError("Unknown TPKT format")

        self.data = packet[4:4+header[2]]
        return self

class COTPConnectionPacket:
    """ COTP Connection Request or Connection Confirm packet (ISO on TCP). RFC 1006
    """
    def __init__(self, dst_ref=0, src_ref=0, dst_tsap=0, src_tsap=0, tpdu_size=0):
        self.dst_ref    = dst_ref
        self.src_ref    = src_ref
        self.dst_tsap   = dst_tsap
        self.src_tsap   = src_tsap
        self.tpdu_size  = tpdu_size

    def pack(self):
        """ make Connection Request Packet
        """
        return pack('!BBHHBBBHBBHBBB',
            17,             # size
            0xe0,           # pdu type: CR
            self.dst_ref,
            self.src_ref,
            0,              # flag
            0xc1, 2, self.src_tsap,
            0xc2, 2, self.dst_tsap,
            0xc0, 1, self.tpdu_size )
    def __str__(self):
        return self.pack()

    def unpack(self, packet):
        """ parse Connection Confirm Packet (header only)
        """
        try:
            size, pdu_type, self.dst_ref, self.src_ref, flags = unpack('!BBHHB', packet[:7])
        except struct.error as e:
            raise S7ProtocolError("Wrong CC packet format")
        if len(packet) != size + 1:
            raise S7ProtocolError("Wrong CC packet size")
        if pdu_type != 0xd0:
            raise S7ProtocolError("Not a CC packet")

        return self

class COTPDataPacket:
    """ COTP Data packet (ISO on TCP). RFC 1006
    """
    def __init__(self, data=''):
        self.data = data
    def pack(self):
        return pack('!BBB',
            2,                      # header len
            0xf0,                   # data packet
            0x80) + str(self.data)
    def unpack(self, packet):
        self.data = packet[ord(packet[0])+1:]
        return self
    def __str__(self):
        return self.pack()

class S7Packet:
    """ S7 packet
    """
    def __init__(self, type=1, req_id=0, parameters='', data=''):
        self.type       = type
        self.req_id     = req_id
        self.parameters = parameters
        self.data       = data
        self.error      = 0

    def pack(self):
        if self.type not in [1,7]:
            raise S7ProtocolError("Unknown pdu type")
        return ( pack('!BBHHHH',
            0x32,                   # protocol s7 magic
            self.type,              # pdu-type
            0,                      # reserved
            self.req_id,            # request id
            len(self.parameters),   # parameters length
            len(self.data)) +       # data length
                 self.parameters +
                 self.data )

    def unpack(self, packet):
        try:
            if ord(packet[1]) in [3,2]:   # pdu-type = response
                header_size = 12
                magic0x32, self.type, reserved, self.req_id, parameters_length, data_length, self.error = unpack('!BBHHHHH', packet[:header_size])
                if self.error:
                    raise S7Error(self.error)
            elif ord(packet[1]) in [1,7]:
                header_size = 10
                magic0x32, self.type, reserved, self.req_id, parameters_length, data_length = unpack('!BBHHHH', packet[:header_size])
            else:
                raise S7ProtocolError("Unknown pdu type (%d)" % ord(packet[1]))
        except (struct.error, IndexError) as e:
            raise S7ProtocolError("Wrong S7 packet format")

        self.parameters = packet[header_size:header_size+parameters_length]
        self.data = packet[header_size+parameters_length:header_size+parameters_length+data_length]
        return self

    def __str__(self):
        return self.pack()


class S7ProtocolError(Exception):
    def __init__(self, message, packet=''):
        self.message = message
        self.packet = packet
    def __str__(self):
        return "[ERROR][S7Protocol] %s" % self.message

class S7Error( Exception ):
    _errors = {
        # s7 data errors
        0x05: 'Address Error',
        0x0a: 'Object does not exist',
        # s7 header errors
        0x8104: 'Context not supported',
        0x8500: 'Wrong PDU size'
    }
    def __init__(self, code):
        self.code = code
    def __str__(self):
        if S7Error._errors.has_key(self.code):
            message = S7Error._errors[self.code]
        else:
            message = 'Unknown error'
        return "[ERROR][S7][0x%x] %s" % (self.code, message)


def Split(ar,size):
    """ split sequence into blocks of given size
    """
    return [ar[i:i+size] for i in range(0, len(ar), size)]

class s7:
    def __init__(self, ip, port, src_tsap=0x200, dst_tsap=0x201, timeout=8):
        self.ip       = ip
        self.port     = port
        self.req_id   = 0
        self.s        = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.dst_ref  = 0
        self.src_ref  = 0x04
        self.dst_tsap = dst_tsap
        self.src_tsap = src_tsap
        self.timeout  = timeout

    def Connect(self):
        """ Establish ISO on TCP connection and negotiate PDU
        """
        #sleep(1)
        self.src_ref = randint(1, 20)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(self.timeout)
        self.s.connect((self.ip, self.port))
        self.s.send(TPKTPacket(COTPConnectionPacket(self.dst_ref, self.src_ref, self.dst_tsap, self.src_tsap, 0x0a)).pack())
        reply = self.s.recv(1024)
        response = COTPConnectionPacket().unpack(TPKTPacket().unpack(reply).data)

        self.NegotiatePDU()

    def Request(self, type, parameters='', data=''):
        """ Send s7 request and receive response
        """
        packet = TPKTPacket(COTPDataPacket(S7Packet(type, self.req_id, parameters, data))).pack()
        self.s.send(packet)
        reply = self.s.recv(1024)
        response = S7Packet().unpack(COTPDataPacket().unpack(TPKTPacket().unpack(reply).data).data)
        if self.req_id != response.req_id:
            raise S7ProtocolError('Sequence ID not correct')
        return response


    def NegotiatePDU(self, pdu=480):
        """ Send negotiate pdu request and receive response. Reply no matter
        """
        response = self.Request(0x01, pack('!BBHHH',
            0xf0,       # function NegotiatePDU
            0x00,       # unknown
            0x01,       # max number of parallel jobs
            0x01,       # max number of parallel jobs
            pdu))      # pdu length

        func, unknown, pj1, pj2, pdu = unpack('!BBHHH', response.parameters)
        return pdu


    def Function(self, type, group, function, data=''):
        parameters = pack('!LBBBB',
            0x00011200 +            # parameter head (magic)
            0x04,                   # parameter length
            0x11,                   # unknown
            type*0x10+group,        # type, function group
            function,               # function
            0x00 )                  # sequence

        data = pack('!BBH', 0xFF, 0x09, len(data)) + data
        response = self.Request(0x07, parameters, data)

        code, transport_size, data_len = unpack('!BBH', response.data[:4])
        if code != 0xFF:
            raise S7Error(code)
        return response.data[4:]

    def ReadSZL(self, szl_id):
        szl_data = self.Function(
            0x04,                   # request
            0x04,                   # szl-functions
            0x01,                   # read szl
            pack('!HH',
                szl_id,             # szl id
                1))                 # szl index

        szl_id, szl_index, element_size, element_count = unpack('!HHHH', szl_data[:8])


        return Split(szl_data[8:], element_size)

class S7Device(Device.TCPDevice):
    """西门子S7设备"""
    DEFAULT_PORTS = [102,]
    PROTOCOL_NAME = 'S7'

    def __init__(self, ip, port = DEFAULT_PORTS[0]):
        super(S7Device, self).__init__(ip, port)
        self.vendor = '西门子'        
        self.protocol = self.PROTOCOL_NAME
            
        self.module = ''
        self.hardware_version = ''
        self.firmware_version = ''
        self.plc_name = ''
        self.module_name = ''
        self.plant_identity = ''
        self.copyright_info = ''
        self.module_sn = ''
        self.os_reserved = ''
        self.module_type = ''
        self.memory_card_sn = ''
        self.cpu_profile = ''
        self.oem_id = ''
        self.module_location = ''
        self.unknown = ''
        
    def BruteTsap(self, src_tsaps=(0x100, 0x200), dst_tsaps=(0x102, 0x200, 0x201), timeout=2):
        for src_tsap in src_tsaps:
            for dst_tsap in dst_tsaps:
                try:
                    con = s7(self.ip, self.port)
                    con.src_tsap = src_tsap
                    con.dst_tsap = dst_tsap
                    con.timeout  = timeout
                    con.Connect()
                    return src_tsap, dst_tsap

                except S7ProtocolError as e:
                    pass

                except socket.error, e:  # 2016/1/28 add by yangyiyin
                    if e.errno in (socket.errno.ECONNABORTED, socket.errno.ECONNRESET):
                        # 10053和10054错误，继续遍历完成所有tsap
                        pass
                    else:
                        # 其他异常则终止尝试
                        return None

        return None

    def GetIdentity(self, src_tsap, dst_tsap, timeout):
        szl_dict = {
            0x11:
                    { 'title': 'Module Identification',
                      'indexes': {
                          1:'module',
                          6:'hardware_version',
                          7:'firmware_version'
                      },
                      'packer': {
                          (1, 6): lambda packet: "{0:s} v.{2:d}.{3:d}".format(*unpack('!20sHBBH', packet)),
                          (7,): lambda packet: "{0:s} v.{3:d}.{4:d}.{5:d}".format(*unpack('!20sHBBBB', packet))
                      }
                    },
            0x1c:
                    { 'title': 'Component Identification',
                      'indexes': {
                          1: 'plc_name',
                          2: 'module_name',
                          3: 'plant_identity',
                          4: 'copyright_info',
                          5: 'module_sn',
                          6: 'os_reservde',
                          7: 'module_type',
                          8: 'memory_card_sn',
                          9: 'cpu_profile',
                          10:'oem_id',
                          11:'module_location'
                      },
                      'packer': {
                          (1, 2, 5): lambda packet: "%s" % packet[:24],
                          (3, 7, 8): lambda packet: "%s" % packet[:32],
                          (4,): lambda packet: "%s" % packet[:26]
                      }
                    }
        }
        con = s7(self.ip, self.port, src_tsap, dst_tsap, timeout)
        con.Connect()

        for szl_id in szl_dict.keys():
            print 1222
            try:
                entities = con.ReadSZL(szl_id)
            except S7Error, e:
                # 保存错误信息， 2016/03/02 add by yangyiyin
                self.fingerprint += '读取SZL[0x%02x]失败: [%s] - %s\n ' % (szl_id, szl_dict[szl_id]['title'], e)
                continue

            indexes = szl_dict[szl_id]['indexes']
            packers = szl_dict[szl_id]['packer']
            for item in entities:
                if len(item)>2:
                    n, = unpack('!H', item[:2])
                    item = item[2:]
                    title = indexes[n] if indexes.has_key(n) else "unknown"

                    try:
                        packers_keys = [ i for i in packers.keys() if n in i ]
                        formated_item = packers[packers_keys[0]](item).strip('\x00')
                    except (struct.error, IndexError) :
                        formated_item = StripUnprintable(item).strip('\x00')

                    #res.append("%s: %s\t(%s)" % (title.ljust(25), formated_item.ljust(30), item.encode('hex')))
                    #res.append("%s: %s" % (title, formated_item.strip().decode('gbk').encode('utf8')))
                    setattr(self, title, formated_item.strip().decode('gbk').encode('utf8'))

        # 匹配指纹

        if any([self.module, self.hardware_version, self.firmware_version,
            self.plc_name, self.module_name, self.plant_identity,
            self.copyright_info, self.module_sn, self.os_reserved,
            self.module_type, self.memory_card_sn, self.cpu_profile,
            self.oem_id, self.module_location]):
            self.fingerprint += '模块: %s \n硬件版本: %s \n固件版本: %s \n' \
                         'PLC名称: %s \n模块名称: %s \n工厂标示: %s\n' \
                         '版权信息: %s \n模块序列号: %s \n系统保留: %s \n' \
                         '模块类型: %s \n内存卡序列号: %s \nCPU模块特性: %s \n' \
                         '制造商ID: %s \n模块位置: %s \n未知信息: %s' % (
                self.module,
                self.hardware_version,
                self.firmware_version,
                self.plc_name,
                self.module_name,
                self.plant_identity,
                self.copyright_info,
                self.module_sn,
                self.os_reserved,
                self.module_type,
                self.memory_card_sn,
                self.cpu_profile,
                self.oem_id,
                self.module_location,
                self.unknown
            )
        result = FingerprintDict.GenericFingerprintDict.match(self.module)
        if result:
            self.type = result[0]
            self.vendor = result[1]
            self.model = result[2]
        else:
            result = FingerprintDict.GenericFingerprintDict.match(self.fingerprint)
            if result:
                self.type = result[0]
                self.vendor = result[1]
                self.model = result[2]

def scan(ip, port, src_tsaps=[0x100, 0x200], dst_tsaps=[0x102, 0x200, 0x201], timeout=None):
    # src_tsaps = [ int(n.strip(), 0) for n in options.src_tsap.split(',') ] if options.src_tsap else [0x100, 0x200]
    # dst_tsaps = [ int(n.strip(), 0) for n in options.dst_tsap.split(',') ] if options.dst_tsap else [0x102, 0x200, 0x201]

    device = S7Device(ip, port)
    result = None
    # tsap = ()
    
    # try:
    #     tsap = device.BruteTsap(src_tsaps, dst_tsaps, timeout)
    # except:  # socket.error as e:
    #     #_logger.info("%s:%d %s" % (ip, port, e))
    #     pass
    #
    # if not tsap:
    #     return None

    # _logger.info( "%s:%d S7comm (src_tsap=0x%x, dst_tsap=0x%x)" % (ip, port, tsap[0], tsap[1]))
    timeout = timeout or device.timeout
    # sometimes unexpected exceptions occures, so try to get identity several time
    for attempt in range(device.retry):
        try:
            tsap = device.BruteTsap(src_tsaps, dst_tsaps, timeout)
            if not tsap:
                continue

            device.GetIdentity(tsap[0], tsap[1], timeout)
            result = device
            #print result
            break

        except:
            pass
        # 
        # except (S7ProtocolError, socket.error) as e:
        #     _logger.error("%s - %s" % (ip, e))
        #     result = None
            
    return result

def addOptions(parser):
    group = OptionGroup(parser, "S7 scanner options")
    group.add_option("--src-tsap", help="Try this src-tsap (list) (default: 0x100,0x200)", type="string", metavar="LIST")
    group.add_option("--dst-tsap", help="Try this dst-tsap (list) (default: 0x102,0x200,0x201)", type="string", metavar="LIST")
    parser.add_option_group(group)

if __name__ == '__main__':
    #print scan('221.15.44.49', 102)
    print scan('10.10.10.50', 102)