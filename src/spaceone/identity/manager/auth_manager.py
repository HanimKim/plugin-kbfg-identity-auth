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

import logging

from spaceone.core.manager import BaseManager
from spaceone.identity.connector.kbfg_connector import KbfgConnector

__all__ = ['AuthManager']
_LOGGER = logging.getLogger(__name__)

class AuthManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kbfg_conn: KbfgConnector = self.locator.get_connector('KbfgConnector')
    
    def get_endpoint(self, options):
        endpoints = self.kbfg_conn.get_endpoint(options)
        return {'metadata': endpoints}

    # def get_plugin_metadata(self, options):
    #     capability = {
    #         'check_endpoint': f'{KB_SSO_URL}{CHECK_URL}',
    #         'authorization_endpoint': f'{KB_SSO_URL}{AUTHORIZATION_URL}',
    #         'token_endpoint': f'{KB_SSO_URL}{TOKEN_URL}'
    #     }
    #     return {'metadata': capability}

    def verify(self, options, secret_data, schema):
        self.kbfg_conn.verify(options, secret_data, schema)

    def login(self, options, secret_data, schema, user_credentials):
        user_data = self.kbfg_conn.login(options, secret_data, schema, user_credentials)
        # _LOGGER.debug(f'[login] {user_data}')
        return user_data

    def find(self, options, secret_data, schema, user_id=None, keyword=None):
        users = self.kbfg_conn.find(options, secret_data, schema, user_id, keyword)
        # _LOGGER.debug(f'[find] {users}')
        return users
