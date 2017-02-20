# Copyright 2014 - Mirantis, Inc.
# Copyright 2015 - StackStorm, Inc.
# Copyright 2016 - Ericsson AB.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import six

import osprofiler.profiler

from kingbirdclient.api import httpclient
from kingbirdclient.api.v1 import quota_class_manager as qcm
from kingbirdclient.api.v1 import quota_manager as qm
from kingbirdclient.api.v1 import sync_manager as sm

_DEFAULT_KINGBIRD_URL = "http://localhost:8118/v1.0"


class Client(object):
    def __init__(self, kingbird_url=None, username=None, api_key=None,
                 project_name=None, auth_url=None, project_id=None,
                 endpoint_type='publicURL', service_type='synchronization',
                 auth_token=None, user_id=None, cacert=None, insecure=False,
                 profile=None, auth_type='keystone', client_id=None,
                 client_secret=None):

        if kingbird_url and not isinstance(kingbird_url, six.string_types):
            raise RuntimeError('Kingbird url should be a string.')

        if auth_url:
            if auth_type == 'keystone':
                (kingbird_url, auth_token, project_id, user_id) = (
                    authenticate(
                        kingbird_url,
                        username,
                        api_key,
                        project_name,
                        auth_url,
                        project_id,
                        endpoint_type,
                        service_type,
                        auth_token,
                        user_id,
                        cacert,
                        insecure
                    )
                )
            else:
                raise RuntimeError(
                    'Invalid authentication type [value=%s, valid_values=%s]'
                    % (auth_type, 'keystone')
                )

        if not kingbird_url:
            kingbird_url = _DEFAULT_KINGBIRD_URL

        if profile:
            osprofiler.profiler.init(profile)

        self.http_client = httpclient.HTTPClient(
            kingbird_url,
            auth_token,
            project_id,
            user_id,
            cacert=cacert,
            insecure=insecure
        )

        # Create all resource managers
        self.quota_manager = qm.quota_manager(self.http_client)
        self.quota_class_manager = qcm.quota_class_manager(self.http_client)
        self.sync_manager = sm.sync_manager(self.http_client)


def authenticate(kingbird_url=None, username=None,
                 api_key=None, project_name=None, auth_url=None,
                 project_id=None, endpoint_type='publicURL',
                 service_type='synchronization', auth_token=None, user_id=None,
                 cacert=None, insecure=False):
    if project_name and project_id:
        raise RuntimeError(
            'Only project name or project id should be set'
        )

    if username and user_id:
        raise RuntimeError(
            'Only user name or user id should be set'
        )

    keystone_client = _get_keystone_client(auth_url)

    keystone = keystone_client.Client(
        username=username,
        user_id=user_id,
        password=api_key,
        token=auth_token,
        tenant_id=project_id,
        tenant_name=project_name,
        auth_url=auth_url,
        endpoint=auth_url,
        cacert=cacert,
        insecure=insecure
    )

    keystone.authenticate()

    token = keystone.auth_token
    user_id = keystone.user_id
    project_id = keystone.project_id

    if not kingbird_url:
        catalog = keystone.service_catalog.get_endpoints(
            service_type=service_type,
            endpoint_type=endpoint_type
        )

        # For Keystone version 'V2.0' and other.
        serv_endpoint = endpoint_type if keystone.version == 'v2.0' else 'url'
        if service_type in catalog:
            service = catalog.get(service_type)
            kingbird_url = service[0].get(
                serv_endpoint) if service else None

    return kingbird_url, token, project_id, user_id


def _get_keystone_client(auth_url):
    if "v2.0" in auth_url:
        from keystoneclient.v2_0 import client
    else:
        from keystoneclient.v3 import client

    return client
