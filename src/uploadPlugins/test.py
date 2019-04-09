
from time import sleep

def scan(ip,port=100):
    print ip,port
    sleep(60)
    toreturn={}
    toreturn['ip']=ip
    return toreturn

