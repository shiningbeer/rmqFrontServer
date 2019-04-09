import requests,sys,json

headers = {
    'upgrade-insecure-requests': "1",
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
}
def scan(target):
    try:
        url = 'http://' + target+'/cgi-bin/index.cgi'#http://192.168.0.135/cgi-bin/index.cgi
        url2='http://' + target+"/cgi-bin/revision.sh"#http://192.168.0.135/cgi-bin/revision.sh
        r = requests.get(url, headers=headers, timeout=1)
        r2 = requests.get(url2, headers=headers, timeout=1)

        if 'EKI-1526-BE Web Server' in r.text:
            html = r2
            try:
                data=html.text.replace("\n"," ").split()
            except:
                data=[]
            dict = {'IP':target,'device': 'EKI-1526-BE', 'firmware_version':data[0]}
            print  json.dumps(dict)
            return  json.dumps(dict)
        else:
            return ""
    except:
        return ""

if __name__=='__main__':
    if len(sys.argv)<2:
        print "Usage: python "+sys.argv[0]+" 192.168.0.134"
        sys.exit()
    else:
        scan(sys.argv[1])
#{"device": "EKI-1526-BE", "IP": "192.168.0.135", "firmware_version": "1.96"}