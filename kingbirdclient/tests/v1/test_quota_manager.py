# Copyright (c) 2016 Ericsson AB.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
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

from kingbirdclient.api.v1 import quota_manager as qm
from kingbirdclient.commands.v1 import quota_manager as quota_cmd
from kingbirdclient.tests import base

QUOTAS_DICT = {
    'Quota': 'fake_item',
    'Limit': '123'
}

QUOTAMANAGER = qm.Quota(mock, QUOTAS_DICT['Quota'],
                        QUOTAS_DICT['Limit'])

DETAIL_QUOTA_DICT = {
    'Quota': 'fake_item',
    'Usage': '123',
    'Limit': '121'
}

DETAIL_QUOTAMANAGER = qm.Quota(mock, DETAIL_QUOTA_DICT['Quota'],
                               DETAIL_QUOTA_DICT['Usage'],
                               DETAIL_QUOTA_DICT['Limit'])

FAKE_TENANT = 'fake_tenant123'


class TestCLIQuotaManagerV1(base.BaseCommandTest):

    def test_list_defaults(self):
        self.client.quota_manager.list_defaults.return_value = [QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.ListDefaults)
        self.assertEqual([('fake_item', '123')], actual_quota[1])

    def test_negative_list_defaults(self):
        self.client.quota_manager.list_defaults.return_value = []
        actual_quota = self.call(quota_cmd.ListDefaults)
        self.assertEqual((('<none>', '<none>'),), actual_quota[1])

    def test_global_limits(self):
        self.client.quota_manager.global_limits.return_value = [QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.GlobalLimits)
        self.assertEqual([('fake_item', '123')], actual_quota[1])

    def test_global_limits_with_tenant_id(self):
        self.client.quota_manager.global_limits.return_value = [QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.GlobalLimits,
                                 app_args=['--tenant', FAKE_TENANT])
        self.assertEqual([('fake_item', '123')], actual_quota[1])

    def test_negative_global_limits(self):
        self.client.quota_manager.global_limits.return_value = []
        actual_quota = self.call(quota_cmd.GlobalLimits)
        self.assertEqual((('<none>', '<none>'),), actual_quota[1])

    def test_update_global_limits(self):
        self.client.quota_manager.\
            update_global_limits.return_value = [QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.UpdateGlobalLimits,
                                 app_args=[FAKE_TENANT, '--ram', '51200'])
        self.assertEqual([('fake_item', '123')], actual_quota[1])

    def test_negative_update_global_limits(self):
        self.client.quota_manager.update_global_limits.return_value = []
        actual_quota = self.call(quota_cmd.UpdateGlobalLimits,
                                 app_args=[FAKE_TENANT, '--ram', '51200'])
        self.assertEqual((('<none>', '<none>'),), actual_quota[1])

    def test_delete_quota(self):
        self.call(quota_cmd.DeleteQuota, app_args=[FAKE_TENANT])
        self.client.quota_manager.delete_quota.\
            assert_called_once_with(FAKE_TENANT)

    def test_sync_quota(self):
        self.call(quota_cmd.SyncQuota, app_args=[FAKE_TENANT])
        self.client.quota_manager.sync_quota.\
            assert_called_once_with(FAKE_TENANT)

    def test_detail_quota_with_tenant_id(self):
        self.client.quota_manager.\
            quota_detail.return_value = [DETAIL_QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.ShowQuotaDetail,
                                 app_args=['--tenant', FAKE_TENANT])
        self.assertEqual([('fake_item', '121', '123')], actual_quota[1])

    def test_detail_quota_without_tenant_id(self):
        self.client.quota_manager.\
            quota_detail.return_value = [DETAIL_QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.ShowQuotaDetail)
        self.assertEqual([('fake_item', '121', '123')], actual_quota[1])
