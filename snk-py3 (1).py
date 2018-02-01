# coding=utf-8
import urlparse

import requests


class Netkeeper(object):
    AES_KEY_PASSWORD = "pass012345678910"
    AES_KEY_SESSION = "jyangzi5@163.com"
    header = {
        'Charset': 'UTF-8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'APP': 'HBZD'
    }

    REDIRECT_ADDR = 'http://114.114.114.114'
    localIpAddress = '100.64.7.37'
    host = '58.53.196.165:8080'

    def loadRedirect(self):
        resp = requests.get(self.REDIRECT_ADDR, allow_redirects=False, timeout=5 * 1000)
        location = resp.headers['Location']
        index = location.index('?')
        if index > 0:
            self.host = location[7:index]
            query_str = location[index + 1:]
            kv = urlparse.parse_qs(query_str)
            self.localIpAddress = kv['userip'][0]
            return True
        else:
            print  "Redirect Url Invalid , url=" + location
        return False

    def getSecret(self):
        try:
            url = 'http://' + self.host + '/wf.do?device=Phone%3AONEPLUS+A3010%5CSDK%3A25&clientType=android&code=1&version=7.1.1&clientip=' + self.localIpAddress
            resp = requests.get(url=url)
            self.AccessToken = resp.text
            # 获取cookies
            self.Cookies = resp.cookies
            return True
        except:
            print "(4/10) 由于异常无法获取拨号参数"
            return False

    def AESEnc(self, sour, key):
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

    def getPasswordEnc(self, password):
        password = self.AESEnc(password, self.AES_KEY_PASSWORD)
        return password

    def getSessionEnc(self, session):
        session = self.AESEnc(session, self.AES_KEY_SESSION)
        return session

    def authenticate(self, username, password):
        try:
            postData = "password=" + self.getPasswordEnc(password) + "&clientType=android&username=" + \
                       username + "&key=" + self.getSessionEnc(
                self.AccessToken) + "&code=8&clientip=" + self.localIpAddress
            headers = self.header
            headers['Content-Length'] = str(len(postData))
            url = 'http://' + self.host + '/wf.do'
            resp = requests.post(url=url, headers=headers, cookies=self.Cookies, data=postData)
            resp.encoding = "GBK"
            print resp.request.headers
            text = resp.text
            print text
            if 'auth00' in text > 0:
                print "连接成功."
                return True
            else:
                print "连接失败"
                return False
        except Exception as e:
            print e
            print "(6/10) 由于异常连接失败"
            return False

    def connect(self, username, password):
        if self.loadRedirect() and self.getSecret() and self.authenticate(username, password):
            print "连接成功"
        else:
            print "连接失败"

    def logout(self, username):
        url = 'http://' + self.host + '/wf.do?username=' + username + '&code=6&clientip=' + self.localIpAddress
        requests.get(url=url, headers=self.header)


if __name__ == '__main__':
    netkeeper = Netkeeper()
    netkeeper.connect('username', 'passwd')