# -*- coding: utf-8 -*-

import time
import random
import hmac, hashlib
import binascii
import base64
from urlparse import urlparse

class Auth(object):

    def __init__(self, secret_id, secret_key):
        self.AUTH_URL_FORMAT_ERROR = -1
        self.AUTH_SECRET_ID_KEY_ERROR = -2

        self._secret_id,self._secret_key = secret_id,secret_key

    def get_info_from_url(self, url):
        info = urlparse(url)
        if info.path :
            parts = info.path.split('/')
            if len(parts) == 5:
                cate = parts[1]
                ver = parts[2]
                appid = parts[3]
                userid = parts[4]
                return {'cate':cate, 'ver':ver, 'appid':appid, 'userid':userid}
            elif len(parts) == 6:
                cate = parts[1]
                ver = parts[2]
                appid = parts[3]
                userid = parts[4]
                fileid = parts[5]
                return {'cate':cate, 'ver':ver, 'appid':appid, 'userid':userid, 'fileid':fileid}
            elif len(parts) == 7:
                cate = parts[1]
                ver = parts[2]
                appid = parts[3]
                userid = parts[4]
                fileid = parts[5]
                oper = parts[6]
                return {'cate':cate, 'ver':ver, 'appid':appid, 'userid':userid, 'fileid':fileid, 'oper':oper}
            else:
                return {}
        else:
            return {}

    def app_sign(self, url, expired=0):
        if not self._secret_id or not self._secret_key:
            return self.AUTH_SECRET_ID_KEY_ERROR

        url_info = self.get_info_from_url(url)
        if len(url_info) == 0:
            return self.AUTH_URL_FORMAT_ERROR

        cate    = url_info['cate']
        ver     = url_info['ver']
        appid   = url_info['appid']
        userid  = url_info['userid']
        if 'oper' in url_info:
            oper = url_info['oper']
        else:
            oper = ''
        if 'fileid' in url_info:
            fileid  = url_info['fileid']
        else:
            fileid = ''

        once_opers = ['del', 'copy']
        if oper in once_opers:
            expired = 0

        puserid = ''
        if userid != '':
            if len(userid) > 64:
                return self.AUTH_URL_FORMAT_ERROR
            puserid = userid

        now = int(time.time())
        rdm = random.randint(0, 999999999)
        plain_text = 'a=' + appid + '&k=' + self._secret_id + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm) + '&u=' + puserid + '&f=' + fileid
        bin = hmac.new(self._secret_key, plain_text, hashlib.sha1)
        s = bin.hexdigest()
        s = binascii.unhexlify(s) + plain_text
        signature = base64.b64encode(s).rstrip()    #生成签名
        return signature

