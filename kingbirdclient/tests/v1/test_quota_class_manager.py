# Copyright (c) 2017 Ericsson AB.
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

from kingbirdclient.api.v1 import quota_class_manager as qcm
from kingbirdclient.commands.v1 import quota_class_manager as quota_class_cmd
from kingbirdclient.tests import base

QUOTAS_DICT = {
    'Quota': 'fake_item',
    'Limit': '123'
}

CLASS_NAME = 'default'

QUOTACLASSMANAGER = qcm.QuotaClass(mock, QUOTAS_DICT['Quota'],
                                   QUOTAS_DICT['Limit'])


class TestCLIQuotaClassManagerV1(base.BaseCommandTest):

    def test_list_quota_class(self):
        self.client.quota_class_manager.\
            list_quota_class.return_value = [QUOTACLASSMANAGER]
        actual_quota = self.call(quota_class_cmd.ListQuotaClass,
                                 app_args=[CLASS_NAME])
        self.assertEqual([('fake_item', '123')], actual_quota[1])

    def test_negative_list_quota_class(self):
        self.client.quota_class_manager.\
            list_quota_class.return_value = []
        actual_quota = self.call(quota_class_cmd.ListQuotaClass,
                                 app_args=[CLASS_NAME])
        self.assertEqual((('<none>', '<none>'),), actual_quota[1])

    def test_update_quota_class(self):
        self.client.quota_class_manager.\
            quota_class_update.return_value = [QUOTACLASSMANAGER]
        actual_quota = self.call(quota_class_cmd.UpdateQuotaClass,
                                 app_args=[CLASS_NAME, '--ram', '51200'])
        self.assertEqual([('fake_item', '123')], actual_quota[1])

    def test_negative_update_quota_class(self):
        self.client.quota_class_manager.\
            quota_class_update.return_value = []
        actual_quota = self.call(quota_class_cmd.UpdateQuotaClass,
                                 app_args=[CLASS_NAME, '--ram', '51200'])
        self.assertEqual((('<none>', '<none>'),), actual_quota[1])

    def test_delete_quota_class(self):
        self.call(quota_class_cmd.DeleteQuotaClass,
                  app_args=[CLASS_NAME])
        self.client.quota_class_manager.delete_quota_class.\
            assert_called_once_with(CLASS_NAME)
