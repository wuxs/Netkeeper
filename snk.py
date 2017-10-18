# coding=utf-8
import urlparse

import requests

AES_KEY_PASSWORD = "pass012345678910"
AES_KEY_SESSION = "jyangzi5@163.com"
header = {
    'Charset': 'UTF-8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'APP': 'HBZD',
    'User-Agent': 'Mozilla/Android/6.0/Letv X620/ffffffff-9404-802f-ffff-ffff89a12926'
}
error_msg = {
    "No Service response": "宽带认证服务异常，请联系10000客服",
    "is Locked": "宽带欠费或者状态不正常（被锁定）",
    "return Account Locked": "账户被锁定，请确认是否欠费",
    "return Credit is ZERO": "账号余额为0，不能登录",
    "ai-Service-Password": "宽带密码错误",
    "ai-vlan-id": "VLAN属性错误，请联系电信维修人员",
    "Called Number": "306 : 客户端已过期，请获取新版使用",
    "NAS-IP-Address": "NAS属性错误，请联系电信维修人员",
    "database authen forbiden": "宽带账号不存在，请联系10000客服",
    "return Illegal Account": "309 : 客户端已过期，请获取新版使用",
    "Null String": "宽带账号为空",
    "return Service Not Available": "宽带认证服务异常，请联系10000客服",
    "comm with Remote Radius Error": "漫游地接入服务无响应",
    "Checking LM, policy": "账号已超过最大在线数量",
    "not from same nas port": "未从指定端口上网，禁止登陆",
    "IsValidClientAccount": "非e信上网错",
    "User-Name not start with": "316 : 客户端已过期，请获取新版使用",
    "return Call Time is ZERO": "账号剩余时间为0，无法连接",
    "Option60,Check Error": "IPTV账号密码错误",
    "ai-school-scope": "319 : 你的帐号不在指定的学校范围，不能登录",
    "ai-Node-Id": "320 : 你的帐号不在指定的学校范围，不能登录",
    "Wrong Password": "321 : 宽带密码错误",
    "EXin User Password Validity Check Failed": "322 : 宽带密码错误",
    "ai-vlan-scope-exclude": "323 : 你的帐号不在指定的学校范围，不能登录",
    "EXin User Password Error": "324 : 宽带密码错误"
}

REDIRECT_ADDR = 'http://114.114.114.114'
localIpAddress = ''
host = '58.53.196.165:8080'


def loadRedirect():
    global AccessToken, Host, LocalIpAddress
    resp = requests.get(REDIRECT_ADDR, allow_redirects=False, timeout=5 * 1000)
    location = resp.headers['Location']
    index = location.index('?')
    if index > 0:
        Host = location[7:index]
        query_str = location[index + 1:]
        kv = urlparse.parse_qs(query_str)
        LocalIpAddress = kv['userip'][0]
        return True
    else:
        print  "Redirect Url Invalid , url=" + location
    return False


def getSecret():
    global Host, LocalIpAddress, AccessToken, Cookies
    try:
        url = 'http://' + Host + '/wf.do?device=Phone%3ALetv+X620%5CSDK%3A23&clientType=android&code=1&version=6.0&clientip=' + LocalIpAddress
        resp = requests.get(url=url)
        AccessToken = resp.text
        # 获取cookies
        Cookies = resp.cookies
        return True
    except:
        print "(4/10) 由于异常无法获取拨号参数"
        return False


def AESEnc(sour, key):
    from Crypto.Cipher import AES
    from Crypto import Random

    sour = sour.encode('utf8')
    key = key.encode('utf8')
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    iv = Random.new().read(bs)
    cipher = AES.new(key, AES.MODE_ECB, iv)
    resData1 = cipher.encrypt(pad(sour))

    resData2 = resData1.encode('hex')
    resData3 = resData2.upper()
    print resData3
    return resData3


def getPasswordEnc(password):
    password = AESEnc(password, AES_KEY_PASSWORD)
    return password


def getSessionEnc(session):
    session = AESEnc(session, AES_KEY_SESSION)
    return session


def authenticate(username, password):
    global Cookies, Host
    try:
        postData = "password=" + getPasswordEnc(password) + "&clientType=android&username=" + \
                   username + "&key=" + getSessionEnc(AccessToken) + "&code=8&clientip=" + LocalIpAddress
        header['Content-Length'] = '219'
        url = 'http://' + Host + '/wf.do'
        resp = requests.post(url=url, headers=header, cookies=Cookies, data=postData)
        resp.encoding = "GBK"
        print resp.request.headers
        text = resp.text
        print text
        if 'auth00' in text > 0:
            print "连接成功."
            return True
        else:
            print "连接失败[" + getErrorMsg(resp) + "]"
            return False
    except Exception as e:
        print e
        print "(6/10) 由于异常连接失败"
        return False


def connect(username, password):
    if loadRedirect() and getSecret() and authenticate(username, password):
        print "连接成功"
    else:
        print "连接失败"


def getErrorMsg(resp):
    return error_msg.get(resp, '')


def logout(username):
    url = 'http://' + Host + '/wf.do?username=' + username + '&code=6&clientip=' + LocalIpAddress
    requests.get(url=url,headers=header)


if __name__ == '__main__':
    connect('username', 'password')
    # logout('username')
    # getPasswordEnc('password')
