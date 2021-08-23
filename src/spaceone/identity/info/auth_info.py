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

import functools
from spaceone.api.identity.plugin import auth_pb2
from spaceone.core.pygrpc.message_type import *

__all__ = ['UserInfo', 'UsersInfo', 'PluginInfo']


def UserInfo(user_data):
    return auth_pb2.UserInfo(**user_data)


def UsersInfo(users, total_count):
    return auth_pb2.UsersInfo(results=list(map(functools.partial(UserInfo), users)), total_count=total_count)


def PluginInfo(result):
    result['metadata'] = change_struct_type(result['metadata'])
    return auth_pb2.PluginInfo(**result)
