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

from kingbirdclient.api.v1 import quota_manager
from kingbirdclient.commands.v1 import quota_manager as quota_cmd
from kingbirdclient.tests import base

QUOTAS_DICT = {
    'Quota': 'fake_item',
    'Limit': '123'
}

QUOTAMANAGER = quota_manager.Quota_Management(mock, QUOTAS_DICT['Quota'],
                                             QUOTAS_DICT['Limit'])


class TestCLIQuotaManagerV1(base.BaseCommandTest):

    def test_list_defaults(self):
        self.client.QuotaManager.list_defaults.return_value = [QUOTAMANAGER]
        actual_quota = self.call(quota_cmd.List)
        self.assertEqual([('fake_item', '123')], actual_quota[1])
