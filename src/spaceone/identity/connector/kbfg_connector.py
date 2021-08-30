#
#   Copyright 2020 The SpaceONE Authors.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import requests
import logging

from spaceone.identity.error import *
from spaceone.core.connector import BaseConnector

__all__ = ["KbfgConnector"]
_LOGGER = logging.getLogger(__name__)

KB_SSO_URL = "http://kbpkiapc.kbstar.com:9080"  # 인증서버 주소
CHECK_URL = "/api/v1/sso"                       # APC(SSO) SERVER 와 통신이 잘 되는지 통신체크 하는 url
AUTHORIZATION_URL = "/sso/signin"               # 통신체크 이후 agent_id로 인증해서 secureToken과 secureSessionId를 받아오는 인증 url
TOKEN_URL = "/sso/validateTicket"               # 토큰이 옳바른 토큰인지 검증하고 uesr 정보를 리턴 해주는 검증 url

class KbfgConnector(BaseConnector):

    def __init__(self, transaction, config):
        super().__init__(transaction, config)

    def get_plugin_metadata(self, options):
        capability = {
            'check_endpoint': KB_SSO_URL + CHECK_URL,
            'authorization_endpoint': KB_SSO_URL + AUTHORIZATION_URL,
            'token_endpoint': KB_SSO_URL + TOKEN_URL
        }
        return {'metadata': capability}

    def verify(self, options, secret_data, schema):
        pass
        # e.g.) This is connection check for Google Authorization Server
        # URL: https://www.googleapis.com/oauth2/v4/token
        # After connection without param.
        # It should return 404
        # authorization_endpoint = self.get_endpoint(options)
        #
        # r = requests.get(authorization_endpoint)
        # if r.status_code == 400:
        #     return "ACTIVE"
        # else:
        #     _LOGGER.debug(f'[verify] status code: {r.status_code}')
        #     raise ERROR_NOT_FOUND(key='authorization_endpoint', value=self.authorization_endpoint)

    def login(self, options, secret_data, schema, user_credentials):
        """
        
        """
        self.get_endpoint(options)

        # Authorization Grant
        access_token = user_credentials.get('secureToken')
        secure_session_id = user_credentials.get('secureSessionId')
        # TODO. requestData의 값을 추가하면, 추가한 값만큼 user에 대한 정보를 더 받을 수 있는지 문의하기.
        #  ex) id,name에서 id,name,email로 email을 추가하면 email의 정보도 받을 수 있는건가?
        request_data = user_credentials.get('requestData')  
        agent_id = user_credentials.get('agentId')
        client_ip = user_credentials.get('clientIP')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }
        # TODO. APC_SERVER 쪽 담당자에게 따로 데이터 보내는 규격이 있는지 문의해보기.
        data = {
            'secureToken': access_token,
            'secureSessionId': secure_session_id,
            'requestData': request_data,
            'agentId': agent_id,
            'clientIP': client_ip
        }

        # Check token information
        # r = requests.post(self.userinfo_endpoint, headers=headers, data=data)
        r = {   # Mocking용 임시 데이터 
            "resultCode": "S200.000",
            "resultMessage": "SUCCESS",
            "user": {
                "id": "test1234",
                "name": "tester"
            },
            "returnUrl": "https://1.1.1.1"
        }

        # if r.resultCode != "S200.000":
        if r['resultCode'] != "S200.000":
            _LOGGER.debug("KbfgConnector return code:%s" % r.resultCode)
            _LOGGER.debug("KbfgConnector return object:%s" % r.json())
            raise ERROR_NOT_FOUND(key='userinfo', value=headers)

        # resultCode == S200.000
        # r2 = r.json()
        r2 = r
        _LOGGER.debug(f'response: {r2}')
        user = r2['user']
        keyList = request_data.split(",")
        # _LOGGER.debug("KbfgConnector user list : %s" % user)
        # _LOGGER.debug("KbfgConnector keyList : %s" % keyList)

        user_info = {}
        for key in keyList:
            if key in user:
                # _LOGGER.debug("###################  key : %s" % key)
                user_info[key] = user[key]
            else:
                raise ERROR_NOT_FOUND(key='user', value='<from access_token>')
        
        result = {}
        if 'id' in user_info:
            result['user_id'] = user_info['id']
        else:
            raise ERROR_NOT_FOUND(key='user', value='<from return user_info>')
        if 'name' in user_info:
            result['name'] = user_info['name']
        else:
            raise ERROR_NOT_FOUND(key='user', value='<from return user_info>')

        return result

    def find(self, options, secret_data, schema, user_id, keyword):

        result = []
        if user_id:
            user_info = {
                'user_id': user_id,
                'state': 'UNIDENTIFIED'
            }
            result.append(user_info)
        else:
            raise ERROR_NOT_FOUND(key='find', value="not found user_id")

        return result
        # e.g.) Find process
        # if secret_data == {}:
        #     # not support find
        #     return self._unidentified_user(user_id, keyword)
        #
        # try:
        #     self.get_endpoint(options)
        #     access_token  = self._get_token_from_credentials(secret_data, schema)
        #     headers={'Content-Type':'application/json',
        #          'Authorization': 'Bearer {}'.format(access_token)}
        #     req_user_find_url = f'{self.user_find_url}?'
        #     if user_id:
        #         req_user_find_url = f'{req_user_find_url}username={user_id}&'
        #     if keyword:
        #         req_user_find_url = f'{req_user_find_url}search={keyword}&'
        #     req_user_find_url = f'{req_user_find_url}max={MAX_FIND}&'
        #     _LOGGER.debug(f'[find] {req_user_find_url}')
        #     resp = requests.get(req_user_find_url, headers=headers)
        #     if resp.status_code == 200:
        #         json_result = resp.json()
        #         return self._parse_user_infos(json_result)
        #
        #     if resp.status_code != 200:
        #         raise ERROR_NOT_FOUND(key='find', value=req_user_find_url)
        # except Exception as e:
        #     _LOGGER.debug(f'[find] {e}')
        #     raise ERROR_INVALID_FIND_REQUEST()
    
    def get_endpoint(self, options):
        """ Find endpoints
        authorization_endpoint
        token_endpoint
        userinfo_endpoint
        """

        self.authorization_endpoint = KB_SSO_URL + AUTHORIZATION_URL
        self.token_endpoint = KB_SSO_URL + TOKEN_URL
        self.check_endpoint = KB_SSO_URL + CHECK_URL

        # result = {}
        # try:
        #     self.authorization_endpoint = options['metadata']['authorization_endpoint']
        #     self.token_endpoint = options['metadata']['token_endpoint']
        #     self.userinfo_endpoint = options['metadata']['userinfo_endpoint']
        #     self.user_find_url = options['metadata']['user_find_url']

        # except Exception as e:
        #     if 'openid-configuration' in options:
        #         config_url = options['openid-configuration']
        #         result = self._parse_configuration(config_url)
        #     else:
        #         raise INVALID_PLUGIN_OPTIONS(options=options)
        #     self.authorization_endpoint = result['authorization_endpoint']
        #     self.token_endpoint = result['token_endpoint']
        #     self.userinfo_endpoint = result['userinfo_endpoint']
        #     self.user_find_url = result['user_find_url']
