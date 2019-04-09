import requests,re,json,sys

headers = {
    'upgrade-insecure-requests': "1",
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
}
def scan(target):
    try:
        url = 'http://' + target
        url2='http://' + target+"/VxWorks/FirmInfo"
        r = requests.get(url, headers=headers, timeout=1)
        r2 = requests.get(url2, headers=headers, timeout=1)
        # print r2.text
        if 'RTU560' in r.text:
            html = r2
            try:
                data=html.text
                name = re.findall('"red">(.*?)<',data)
                version=re.findall('<br>(.*)</font>',data,re.S)
                version = re.findall('<br>\\\\n(.*) ', str(version), re.S)
                # print  name[0],version[0]
            except:
                name = []
                version = []
            dict = {'IP':target,'device': 'RTU560', 'firmware_name': name[0].replace(" ",""), 'firmware_version': version[0]}
            print  json.dumps(dict)
            return  json.dumps(dict)
        else:
            return ""
    except:
        return ""

# scan("10.30.11.128")

if __name__=='__main__':
    if len(sys.argv)<2:
        print "Usage: python "+sys.argv[0]+" 192.168.0.134"
        sys.exit()
    else:
        scan(sys.argv[1])

