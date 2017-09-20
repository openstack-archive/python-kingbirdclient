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

import keystoneauth1.identity.generic as auth_plugin
from keystoneauth1 import session as ks_session

from kingbirdclient.api import httpclient
from kingbirdclient.api.v1 import quota_class_manager as qcm
from kingbirdclient.api.v1 import quota_manager as qm
from kingbirdclient.api.v1 import sync_manager as sm

import osprofiler.profiler

import six


_DEFAULT_KINGBIRD_URL = "http://localhost:8118/v1.0"


class Client(object):
    """Class where the communication from KB to Keystone happens."""

    def __init__(self, kingbird_url=None, username=None, api_key=None,
                 project_name=None, auth_url=None, project_id=None,
                 endpoint_type='publicURL', service_type='synchronization',
                 auth_token=None, user_id=None, cacert=None, insecure=False,
                 profile=None, auth_type='keystone', client_id=None,
                 client_secret=None, session=None, **kwargs):
        """Kingbird communicates with Keystone to fetch necessary values."""
        if kingbird_url and not isinstance(kingbird_url, six.string_types):
            raise RuntimeError('Kingbird url should be a string.')

        if auth_url or session:
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
                        session,
                        cacert,
                        insecure,
                        **kwargs
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
        self.quota_manager = qm.QuotaManager(self.http_client)
        self.quota_class_manager = qcm.QuotaClassManager(self.http_client)
        self.sync_manager = sm.SyncManager(self.http_client)


def authenticate(kingbird_url=None, username=None,
                 api_key=None, project_name=None, auth_url=None,
                 project_id=None, endpoint_type='publicURL',
                 service_type='synchronization', auth_token=None, user_id=None,
                 session=None, cacert=None, insecure=False, **kwargs):
    """Get token, project_id, user_id and Endpoint."""
    if project_name and project_id:
        raise RuntimeError(
            'Only project name or project id should be set'
        )

    if username and user_id:
        raise RuntimeError(
            'Only user name or user id should be set'
        )
    user_domain_name = kwargs.get('user_domain_name')
    user_domain_id = kwargs.get('user_domain_id')
    project_domain_name = kwargs.get('project_domain_name')
    project_domain_id = kwargs.get('project_domain_id')

    if session is None:
        if auth_token:
            auth = auth_plugin.Token(
                auth_url=auth_url,
                token=auth_token,
                project_id=project_id,
                project_name=project_name,
                project_domain_name=project_domain_name,
                project_domain_id=project_domain_id)

        elif api_key and (username or user_id):
            auth = auth_plugin.Password(
                auth_url=auth_url,
                username=username,
                user_id=user_id,
                password=api_key,
                project_id=project_id,
                project_name=project_name,
                user_domain_name=user_domain_name,
                user_domain_id=user_domain_id,
                project_domain_name=project_domain_name,
                project_domain_id=project_domain_id)

        else:
            raise RuntimeError('You must either provide a valid token or'
                               'a password (api_key) and a user.')
        if auth:
            session = ks_session.Session(auth=auth)

    if session:
        token = session.get_token()
        project_id = session.get_project_id()
        user_id = session.get_user_id()
        if not kingbird_url:
            kingbird_url = session.get_endpoint(
                service_type=service_type,
                endpoint_type=endpoint_type)

    return kingbird_url, token, project_id, user_id
