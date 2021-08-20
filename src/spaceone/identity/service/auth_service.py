# -*- coding: utf-8 -*-
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

from spaceone.core.error import *
from spaceone.core.service import *

from spaceone.identity.error import *
from spaceone.identity.manager.auth_manager import AuthManager

_LOGGER = logging.getLogger(__name__)

AUTHORIZATION_POSTFIX = 'sso/signin'
TOKEN_POSTFIX = 'sso/validateTicket'

@authentication_handler
class AuthService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options'])
    def init(self, params):
        """ verify options
        Args:
            params
              - options

        Returns:
            - metadata
        Raises:
            ERROR_NOT_FOUND:
        """
        manager = self.locator.get_manager('AuthManager')
        options = params['options']
        self._check_options(options)
        capability = self._create_metadata(options['auth_url'])
        return {'metadata': capability}

    @transaction
    @check_required(['options','secret_data'])
    def verify(self, params):
        """ verify options
        Args:
            params
              - options
              - secret_data: client_id, client_secret
              - schema: oauth2_client_credentials

        Returns:

        Raises:
            ERROR_NOT_FOUND:
        """
        manager = self.locator.get_manager('AuthManager')
        options = params['options']
        secret_data = params.get('secret_data', {})
        schema = params.get('schema', '')
        manager.verify(options, secret_data, schema)
        return {}

    @transaction
    @check_required(['options','secret_data'])
    def find(self, params):
        """ verify options
        Args:
            params
              - options
              - secret_data: may be empty dictionary
              - schema
              - user_id
              - keyword
        Returns:

        Raises:
            ERROR_NOT_FOUND:
        """
        _LOGGER.debug(f'[find] params: {params}')
        manager = self.locator.get_manager('AuthManager')
        options = params['options']
        secret_data = params.get('secret_data', {})
        schema = params.get('schema', '')

        # collect plugins_info
        user_id = params.get('user_id', None)
        keyword = params.get('keyword', None)
        if user_id == None and keyword == None:
            raise ERROR_INVALID_FIND_REQUEST()

        user_infos = manager.find(options, secret_data, schema, user_id, keyword)
        _LOGGER.debug(f'[find] user_info: {user_infos}')
        if len(user_infos) == 0:
            raise ERROR_NOT_FOUND_USERS()

        return user_infos, len(user_infos)

    @transaction
    @check_required(['options','secret_data', 'user_credentials'])
    def login(self, params):
        """ verify options
        options = configuration (https://<domain>/auth/realms/<Realm>/.well-known/openid-configuration)
        Args:
            params
              - options
              - secret_data
              - schema
              - user_credentials

        Returns:

        Raises:
            ERROR_NOT_FOUND:
        """
        manager = self.locator.get_manager('AuthManager')
        options = params['options']
        credentials = params['secret_data']
        user_credentials = params['user_credentials']
        return manager.login(options, credentials, user_credentials)

    def _check_options(self, options):
        """
        Check options

        required fields:
            auth_type: kbfg_sso
            agent_id: xxxxx
            auth_url: http://1.1.1.11
        """
        auth_type = options.get('auth_type', "")
        if auth_type != "kbfg_sso":
            raise INVALID_PLUGIN_OPTIONS(options=auth_type)
        agent_id = options.get('agent_id', None)
        if agent_id == None:
            raise INVALID_PLUGIN_OPTIONS(options="no agent_id")
        auth_url = options.get('auth_url', None)
        if auth_url == None:
            raise INVALID_PLUGIN_OPTIONS(options="no auth_url")
        return True

    def _create_metadata(self, auth_url):
        """
        return
            authorization_endpoint: auth_url/sso/signin
            token_endpoint: auth_url/sso/validateTicket
        """
        endpoints = {
            'authorization_endpoint': f'{auth_url}/{AUTHORIZATION_POSTFIX}',
            'token_endpoint': f'{auth_url}/{TOKEN_POSTFIX}'
        }
        return endpoints

