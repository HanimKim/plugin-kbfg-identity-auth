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


class KbfgConnector(BaseConnector):

    def __init__(self, transaction, config):
        super().__init__(transaction, config)

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
        headers = {     # TODO. user_credentials안에 데이터를 헤더에 어떻게 담으면 되나!?
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token)
        }

        # Check token information
        # r = requests.get(self.userinfo_endpoint, headers=headers)
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
        result['user_id'] = user_info['id']
        result['name'] = user_info['name']
        # result['email'] = ""
        # result['mobile'] = ""     # TODO. 나머지 값들은 없어도 되는가?
        # result['group'] = ""
        result['state'] = "UNIDENTIFIED"

        return result

    def find(self, options, secret_data, schema, user_id, keyword):

        return []
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
        # TODO. 여기 구조를 보면 처음 init() 에서 response값으로 주는 metadata 값을
        #       그대로 화면에서 들고 있다가 다시 options 값에 넣어서 login()을 호출하는
        #       것 같은데, 그 구조가 맞는 것인가!?

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
