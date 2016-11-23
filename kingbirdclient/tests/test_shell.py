# Copyright 2016 EricssonAB.
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

import mock

from kingbirdclient.tests import base_shell_test as base


class TestShell(base.BaseShellTests):

    @mock.patch('kingbirdclient.api.client.determine_client_version')
    def test_kingbird_version(self, mock):
        self.shell(
            '--os-kingbird-version=v1 quota-defaults'
        )
        self.assertTrue(mock.called)
        kingbird_version = mock.call_args
        self.assertEqual('v1', kingbird_version[0][0])

    @mock.patch('kingbirdclient.api.client.determine_client_version')
    def test_default_kingbird_version(self, mock):
        default_version = 'v1.0'
        self.shell('quota defaults')
        self.assertTrue(mock.called)
        kingbird_version = mock.call_args
        self.assertEqual(default_version, kingbird_version[0][0])

    @mock.patch('kingbirdclient.api.client.client')
    def test_env_variables(self, mock):
        self.shell(
            '--os-auth-url=https://127.0.0.1:35357/v3 '
            '--os-username=admin '
            '--os-password=1234 '
            '--os-tenant-name=admin '
            'quota defaults'
        )
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('https://127.0.0.1:35357/v3', params[1]['auth_url'])
        self.assertEqual('admin', params[1]['username'])
        self.assertEqual('admin', params[1]['project_name'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_env_without_auth_url(self, mock):
        self.shell(
            '--os-username=admin '
            '--os-password=1234 '
            '--os-tenant-name=admin '
            'quota defaults'
        )
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('', params[1]['auth_url'])
        self.assertEqual('admin', params[1]['username'])
        self.assertEqual('admin', params[1]['project_name'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_kb_service_type(self, mock):
        self.shell('--os-service-type=synchronization')
        self.assertTrue(mock.called)
        parameters = mock.call_args
        self.assertEqual('synchronization', parameters[1]['service_type'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_kb_default_service_type(self, mock):
        self.shell('quota defaults')
        self.assertTrue(mock.called)
        params = mock.call_args
        # Default service type is synchronization
        self.assertEqual('synchronization', params[1]['service_type'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_kb_endpoint_type(self, mock):
        self.shell('--os-kingbird-endpoint-type=adminURL quota-defaults')
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('adminURL', params[1]['endpoint_type'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_kb_default_endpoint_type(self, mock):
        self.shell('quota defaults')
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('publicURL', params[1]['endpoint_type'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_os_auth_token(self, mock):
        self.shell(
            '--os-auth-token=abcd1234 '
            'quota defaults'
        )
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('abcd1234', params[1]['auth_token'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_command_without_kingbird_url(self, mock):
        self.shell(
            'quota defaults'
        )
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('', params[1]['kingbird_url'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_command_with_kingbird_url(self, mock):
        self.shell(
            '--os-kingbird-url=http://localhost:8118/v1 quota-defaults'
        )
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('http://localhost:8118/v1',
                         params[1]['kingbird_url'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_command_without_project_name(self, mock):
        self.shell(
            'quota defaults'
        )
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('', params[1]['project_name'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_kingbird_profile(self, mock):
        self.shell('--profile=SECRET_HMAC_KEY quota defaults')
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('SECRET_HMAC_KEY', params[1]['profile'])

    @mock.patch('kingbirdclient.api.client.client')
    def test_kingbird_without_profile(self, mock):
        self.shell('quota defaults')
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual(None, params[1]['profile'])
