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

from spaceone.core.service import *

from spaceone.identity.error import *
from spaceone.identity.manager.auth_manager import AuthManager

_LOGGER = logging.getLogger(__name__)

class AuthService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.auth_mgr: AuthManager = self.locator.get_manager('AuthManager')

    @transaction
    @check_required(['options'])
    def init(self, params):
        """ Init plugin
        Args:
            params (dict): {
                    'options': 'dict'
                }

        Returns:
            metadata (dict)

        """

        options = params['options']

        self._check_options(options)

        return self.auth_mgr.get_plugin_metadata(options)

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """ Verify plugin
        Args:
            params (dict): {
                    'options': 'dict',
                    'secret_data': 'dict',
                    'schema': 'string'
                }

        Returns:
            None

        """

        options = params['options']
        secret_data = params['secret_data']
        schema = params.get('schema')

        self._check_options(options)
        self.auth_mgr.verify(options, secret_data, schema)

    @transaction
    @check_required(['options', 'secret_data'])
    def find(self, params):
        """ Find user
        Args:
            params (dict): {
                    'options': 'dict',
                    'secret_data': 'dict',
                    'schema': 'string',
                    'user_id': 'string',
                    'keyword': 'string'
                }

        Returns:
            users (list)

        """

        options = params['options']
        secret_data = params['secret_data']
        schema = params.get('schema')

        user_id = params.get('user_id')
        keyword = params.get('keyword')
        self._check_find_options(user_id, keyword)

        user_infos = self.auth_mgr.find(options, secret_data, schema, user_id, keyword)
        return user_infos, len(user_infos)

    @transaction
    @check_required(['options', 'secret_data', 'user_credentials'])
    def login(self, params):
        """ Login user
        Args:
            params (dict): {
                    'options': 'dict',
                    'secret_data': 'dict',
                    'schema': 'string',
                    'user_credentials': 'dict'
                }

        ex) { "options": {}, "secret_data": {}, "user_credentials": {"secureToken": "1234", "secureSessionId": "1111", "requestData": "id,name", "agentId": "2222", "clientIP": "1.1.1.1"}  }

        Returns:
            user_data (dict)

        """

        options = params['options']
        secret_data = params['secret_data']
        schema = params.get('schema')
        user_credentials = params['user_credentials']

        self._check_login_options(user_credentials)

        return self.auth_mgr.login(options, secret_data, schema, user_credentials)

    @staticmethod
    def _check_options(options: dict):
        if options.get('auth_type') is None:
            raise ERROR_REQUIRED_PARAMETER(key='plugin_info.options.auth_type')
        elif options.get('auth_type') != 'kbfg_sso':
            raise ERROR_PLUGIN_OPTIONS(reason='auth_type require kbfg_sso.')

        if options.get('agent_id') is None:
            raise ERROR_REQUIRED_PARAMETER(key='plugin_info.options.agent_id')

    @staticmethod
    def _check_find_options(user_id, keyword):
        if user_id is None and keyword is None:
            raise ERROR_REQUIRED_FIND_OPTIONS()

    @staticmethod
    def _check_login_options(user_credentials: dict):
        if user_credentials.get('secureToken') is None:
            raise ERROR_REQUIRED_PARAMETER(key='plugin_info.user_credentials.secureToken')

        # if user_credentials.get('secureSessionId') is None:
        #     raise ERROR_REQUIRED_PARAMETER(reason='plugin_info.user_credentials.secureSessionId')
        
        if user_credentials.get('requestData') is None:
            raise ERROR_REQUIRED_PARAMETER(key='plugin_info.user_credentials.requestData')
        
        if user_credentials.get('agentId') is None:
            raise ERROR_REQUIRED_PARAMETER(key='plugin_info.user_credentials.agentId')
        
        if user_credentials.get('clientIP') is None:
            raise ERROR_REQUIRED_PARAMETER(key='plugin_info.user_credentials.clientIP')
