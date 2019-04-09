# -*- coding: utf-8 -*-
'''
2016-4-27 解决reason 编码错误问题，将获取的所有数据在存储时都设置为unicode编码

'''
import httplib
import socket
import os
import json
#import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import chardet
import re
import ssl

'''
这里因为存在title不规则的情况，示例 <title>...</title >  这里多个空格
或者<title>... title> 
或者title是大写
等等情况
'''
def parsing(txt):
    if txt.find('<title>') != -1: #content has title
        #tt=txt.split('<title')[1]
        #title=tt.split('title')[0]
        title = txt.split('title')[1]
        title = title[1:-2]   #remove > and </
    elif txt.find('<TITLE>') != -1:   #content has TITLE
        #tt=txt.split('<TITLE>')[1]
        #title=tt.split('</TITLE>')[0]
        title = txt.split('TITLE')[1]
        title = title[1:-2]
    else:
        title=''
    return title

def scan(ip,port = 80):
    protocol = 'http'
    
   
    dict_header = {}
    http_version = 'HTTP/1.0'   #http version default is 'HTTP/1.0'
    html_chardet = 'utf-8'      #the html chardet default is utf-8
    try:
        
        print "get the ip %s http response" %(ip)
        if protocol=='https':
            conn = httplib.HTTPSConnection(ip, port, timeout=10, context=ssl._create_unverified_context(),)
        else:
            conn = httplib.HTTPConnection(ip, port, timeout=10)
        #conn = httplib.HTTPConnection(ip, port, timeout=10)
        conn.request('GET', '/')
        res = conn.getresponse()
        if res:
            if res.version == 11:
                http_version = 'HTTP/1.1'

            dict_header['http_version'] = str(http_version)
            
            '''
            这里原本计划将message转为字典存储
            '''
            #encodedjson = json.dumps(str(res.msg))     #message to json
            #dict_msg = eval(encodedjson)               #json to dict
            
            
            #dict_header['message'] = dict_msg
            
            content = res.read()
            #print 'res.read', content
            if not content:     #html is none
                print "content is none"
                dict_header['title'] = u'none, because status_code maybe is 302'
            else:
                try:
                    title = parsing(content)
                    print 'parsing:', title
                    #print content
                    content_chardet = chardet.detect(content)
                    print content_chardet['confidence']
                    if content_chardet['confidence'] >= 0.6:    #confidence >= 0.7
                        print content_chardet['encoding']     
                        html_chardet = content_chardet['encoding']
                    
                except:
                    print "title or chardet have no data"
                    title = 'none'
                print html_chardet
                dict_header['title'] = title.decode(encoding=html_chardet)      #decode the title
                #print 'title:', dict_header['title'].encode('utf-8')
            dict_header['status'] = str(res.status).decode(encoding=html_chardet)      #The coding of all string is unicode 
            dict_header['reason'] = str(res.reason).decode(encoding=html_chardet)
            dict_header['message'] = str(res.msg).decode(encoding=html_chardet)
            dict_header['html'] = content
            return (dict_header)

    except Exception,e:
        print 'failed:',e
        string = 'httpresponse ' + str(e)
        #string = 'httpresponse'
        dict_header['error'] = string.decode('utf-8')   #解码，确保所有写入数据为unicode编码
        #print "dict_header['error']", dict_header['error']
        #print type(string)
        #encoding = 'error'
        return (dict_header)

if __name__ == '__main__':
    ip = '116.53.69.114'
    result = {}
    result = scan(ip)
    print result