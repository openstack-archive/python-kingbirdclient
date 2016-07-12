# Copyright 2016 - Ericsson AB
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


def client(kingbird_url=None, username=None, api_key=None,
           project_name=None, auth_url=None, project_id=None,
           endpoint_type='publicURL', service_type='synchronization',
           auth_token=None, user_id=None, cacert=None, insecure=False,
           profile=None):

        if kingbird_url and not isinstance(kingbird_url, six.string_types):
            raise RuntimeError('Kingbird url should be a string.')

        return None


def determine_client_version(kingbird_version):
    if kingbird_version.find("v1") != -1:
        return 2

    raise RuntimeError("Cannot determine Kingbird API version")
