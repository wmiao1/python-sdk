# -*- coding: utf-8 -*-

import os.path
import time
import requests
from tencentyun import conf
from .auth import Auth

class Image(object):

    def __init__(self, appid, secret_id, secret_key):
        self.IMAGE_FILE_NOT_EXISTS = -1
        self.IMAGE_NETWORK_ERROR = -2
        self.IMAGE_PARAMS_ERROR = -3

        self.EXPIRED_SECONDS = 2592000
        self._secret_id,self._secret_key = secret_id,secret_key
        conf.set_app_info(appid, secret_id, secret_key)


    def upload(self, filepath, userid=0, magic_context=''):
        filepath = os.path.abspath(filepath);
        if os.path.exists(filepath):
            expired = int(time.time()) + self.EXPIRED_SECONDS
            url = self.generate_res_url(userid)
            auth = Auth(self._secret_id, self._secret_key)
            sign = auth.app_sign(url, expired)
            size = os.path.getsize(filepath)

            data = {}
            if magic_context:
                data['MagicContext'] = magic_context

            headers = {
                'Authorization':'QCloud '+sign,
                'User-Agent':conf.get_ua(),
            }

            files = {'FileContent': open(filepath, 'rb')}

            r = {}
            try:
                r = requests.post(url, data=data, headers=headers, files=files)
                ret = r.json()
            except Exception as e:
                if r:
                    return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}
                else:
                    return {'httpcode':0, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}
            
            if 'code' in ret:
                if 0 == ret['code']:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{
                            'url':ret['data']['url'],
                            'download_url':ret['data']['download_url'],
                            'fileid':ret['data']['fileid'],
                        }
                    }
                else:
                    return {
                        'httpcode':r.status_code, 
                        'code':ret['code'], 
                        'message':ret['message'], 
                        'data':{}
                    }
            else:
                return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

        else:
            return {'httpcode':0, 'code':self.IMAGE_FILE_NOT_EXISTS, 'message':'file not exists', 'data':{}}

    def stat(self, fileid, userid=0):
        if not fileid:
            return {'httpcode':0, 'code':self.IMAGE_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid)
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.get(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{
                        'download_url':ret['data']['file_url'],
                        'fileid':ret['data']['file_fileid'],
                        'upload_time':ret['data']['file_upload_time'],
                        'size':ret['data']['file_size'],
                        'md5':ret['data']['file_md5'],
                        'width':ret['data']['photo_width'],
                        'height':ret['data']['photo_height'],
                    }
                }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{}
                }
        else:
            return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}

    def copy(self, fileid, userid=0):
        if not fileid:
            return {'httpcode':0, 'code':self.IMAGE_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid, 'copy')
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.post(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{
                        'url':ret['data']['url'],
                        'download_url':ret['data']['download_url'],
                    },
                }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
        else:
            return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}


    def delete(self, fileid, userid=0):
        if not fileid:
            return {'httpcode':0, 'code':self.IMAGE_PARAMS_ERROR, 'message':'params error', 'data':{}}

        expired = int(time.time()) + self.EXPIRED_SECONDS
        url = self.generate_res_url(userid, fileid, 'del')
        auth = Auth(self._secret_id, self._secret_key)
        sign = auth.app_sign(url, expired)

        headers = {
            'Authorization':'QCloud '+sign,
            'User-Agent':conf.get_ua(),
        }

        r = {}
        try:
            r = requests.post(url, headers=headers)
            ret = r.json()
        except Exception as e:
            if r:
                return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}
            else:
                return {'httpcode':0, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(e), 'data':{}}

        if 'code' in ret:
            if 0 == ret['code']:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
            else:
                return {
                    'httpcode':r.status_code, 
                    'code':ret['code'], 
                    'message':ret['message'], 
                    'data':{},
                }
        else:
            return {'httpcode':r.status_code, 'code':self.IMAGE_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}


    def generate_res_url(self, userid=0, fileid='', oper=''):
        app_info = conf.get_app_info()
        if fileid:
            if oper:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid) + '/' + oper
            else:
                return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid) + '/' + str(fileid)
        else:
            return app_info['end_point'] + str(app_info['appid']) + '/' + str(userid)

