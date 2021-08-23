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
        # e.g.) Login process
        # authorization_endpoint = self.get_endpoint(options)
        # Authorization Grant
        # access_token = user_credentials.get('access_token')
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Bearer {}'.format(access_token)
        # }
        # Check token information
        # r = requests.get(self.userinfo_endpoint, headers=headers)
        # if r.status_code != 200:
        #     _LOGGER.debug("KbfgConnector return code:%s" % r.status_code)
        #     _LOGGER.debug("KbfgConnector return code:%s" % r.json())
        #     raise ERROR_NOT_FOUND(key='userinfo', value=headers)
        # status_code == 200
        # r2 = r.json()
        # _LOGGER.debug(f'response: {r2}')
        # result = {}
        # if 'email' in r2:
        #     result['email'] = r2['email']
        #     result['user_id'] = r2['email']
        #     if 'preferred_username' in r2:
        #         result['name'] = r2['preferred_username']
        #     result['state'] = 'ENABLED'
        #     return result
        # raise ERROR_NOT_FOUND(key='user', value='<from access_token>')
        pass

    def find(self, options, secret_data, schema, user_id, keyword):
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
        pass
