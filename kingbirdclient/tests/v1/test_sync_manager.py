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

from oslo_utils import timeutils
from oslo_utils import uuidutils

from kingbirdclient.api.v1 import sync_manager as sm
from kingbirdclient.commands.v1 import sync_manager as sync_cmd
from kingbirdclient.tests import base

TIME_NOW = timeutils.utcnow().isoformat()
ID = uuidutils.generate_uuid()
ID_1 = uuidutils.generate_uuid()
FAKE_STATUS = 'SUCCESS'
ACTIVE_FAKE_STATUS = 'IN_PROGRESS'
FAKE_RESOURCE = 'fake_item'
FAKE_SOURCE_REGION = 'fake_region_1'
FAKE_TARGET_REGION = 'fake_region_2'
FAKE_RESOURCE_TYPE = 'fake_resource'

RESOURCE_DICT = {
    'ID': ID,
    'STATUS': FAKE_STATUS,
    'CREATED_AT': TIME_NOW,
    'UPDATED_AT': TIME_NOW
}

ACTIVE_RESOURCE_DICT = {
    'ID': ID,
    'STATUS': ACTIVE_FAKE_STATUS,
    'CREATED_AT': TIME_NOW,
    'UPDATED_AT': TIME_NOW
}

SYNCMANAGER = sm.Resource(mock, id=RESOURCE_DICT['ID'],
                          status=RESOURCE_DICT['STATUS'],
                          created_at=RESOURCE_DICT['CREATED_AT'],
                          updated_at=RESOURCE_DICT['UPDATED_AT'])

ACTIVE_SYNCMANAGER = sm.Resource(mock, id=ACTIVE_RESOURCE_DICT['ID'],
                                 status=ACTIVE_RESOURCE_DICT['STATUS'],
                                 created_at=ACTIVE_RESOURCE_DICT['CREATED_AT'],
                                 updated_at=ACTIVE_RESOURCE_DICT['UPDATED_AT'])

DETAIL_RESOURCE_DICT = {
    'RESOURCE': FAKE_RESOURCE,
    'SOURCE_REGION': FAKE_SOURCE_REGION,
    'TARGET_REGION': FAKE_TARGET_REGION,
    'RESOURCE_TYPE': FAKE_RESOURCE_TYPE,
    'STATUS': FAKE_STATUS,
    'CREATED_AT': TIME_NOW,
    'UPDATED_AT': TIME_NOW
}

DETAIL_RESOURCEMANAGER = sm.Resource(
    mock, resource_name=DETAIL_RESOURCE_DICT['RESOURCE'],
    source_region=DETAIL_RESOURCE_DICT['SOURCE_REGION'],
    target_region=DETAIL_RESOURCE_DICT['TARGET_REGION'],
    resource_type=DETAIL_RESOURCE_DICT['RESOURCE_TYPE'],
    status=DETAIL_RESOURCE_DICT['STATUS'],
    created_at=DETAIL_RESOURCE_DICT['CREATED_AT'],
    updated_at=DETAIL_RESOURCE_DICT['UPDATED_AT'])

SYNC_RESOURCEMANAGER = sm.Resource(mock, id=RESOURCE_DICT['ID'],
                                   status=RESOURCE_DICT['STATUS'],
                                   created_at=RESOURCE_DICT['CREATED_AT'])


class TestCLISyncManagerV1(base.BaseCommandTest):

    def test_sync_jobs_list(self):
        self.client.sync_manager.list_sync_jobs.return_value = [SYNCMANAGER]
        actual_call = self.call(sync_cmd.SyncList)
        self.assertEqual([(ID, FAKE_STATUS, TIME_NOW, TIME_NOW)],
                         actual_call[1])

    def test_negative_sync_jobs_list(self):
        self.client.sync_manager.list_sync_jobs.return_value = []
        actual_call = self.call(sync_cmd.SyncList)
        self.assertEqual((('<none>', '<none>', '<none>', '<none>'),),
                         actual_call[1])

    def test_active_sync_jobs_list(self):
        self.client.sync_manager.list_sync_jobs.\
            return_value = [ACTIVE_SYNCMANAGER]
        actual_call = self.call(sync_cmd.SyncList, app_args=['--active'])
        self.assertEqual([(ID, ACTIVE_FAKE_STATUS, TIME_NOW, TIME_NOW)],
                         actual_call[1])

    def test_active_sync_jobs_negative(self):
        self.client.sync_manager.list_sync_jobs.\
            return_value = [ACTIVE_SYNCMANAGER]
        self.assertRaises(SystemExit, self.call,
                          sync_cmd.SyncList, app_args=['--fake'])

    def test_delete_sync_job_with_job_id(self):
        self.call(sync_cmd.SyncDelete, app_args=[ID])
        self.client.sync_manager.delete_sync_job.\
            assert_called_once_with(ID)

    def test_delete_multiple_sync_jobs(self):
        self.call(sync_cmd.SyncDelete, app_args=[ID, ID_1])
        self.assertEqual(2,
                         self.client.sync_manager.delete_sync_job.call_count)

    def test_delete_sync_job_without_job_id(self):
        self.assertRaises(SystemExit, self.call,
                          sync_cmd.SyncDelete, app_args=[])

    def test_detail_sync_job_with_job_id(self):
        self.client.sync_manager.sync_job_detail.\
            return_value = [DETAIL_RESOURCEMANAGER]
        actual_call = self.call(sync_cmd.SyncShow, app_args=[ID])
        self.assertEqual([(FAKE_RESOURCE, FAKE_SOURCE_REGION,
                           FAKE_TARGET_REGION, FAKE_RESOURCE_TYPE,
                           FAKE_STATUS, TIME_NOW, TIME_NOW)], actual_call[1])

    def test_detail_sync_job_negative(self):
        self.client.sync_manager.sync_job_detail.return_value = []
        actual_call = self.call(sync_cmd.SyncShow, app_args=[ID])
        self.assertEqual((('<none>', '<none>', '<none>', '<none>',
                           '<none>', '<none>', '<none>'),), actual_call[1])

    def test_detail_sync_job_without_job_id(self):
        self.assertRaises(SystemExit, self.call,
                          sync_cmd.SyncShow, app_args=[])

    def test_resource_sync_without_force(self):
        self.client.sync_manager.sync_resources.\
            return_value = [SYNC_RESOURCEMANAGER]
        actual_call = self.call(
            sync_cmd.ResourceSync, app_args=[
                '--resource_type', FAKE_RESOURCE_TYPE,
                '--resources', FAKE_RESOURCE,
                '--source', FAKE_SOURCE_REGION, '--target',
                FAKE_TARGET_REGION])
        self.assertEqual([(ID, FAKE_STATUS, TIME_NOW)], actual_call[1])

    def test_resource_sync_without_resources(self):
        self.client.sync_manager.sync_resources.\
            return_value = [SYNC_RESOURCEMANAGER]
        self.assertRaises(
            SystemExit, self.call, sync_cmd.ResourceSync, app_args=[
                '--resource_type', FAKE_RESOURCE_TYPE,
                '--source', FAKE_SOURCE_REGION,
                '--target', FAKE_TARGET_REGION])

    def test_resource_sync_without_resource_type(self):
        self.client.sync_manager.sync_resources.\
            return_value = [SYNC_RESOURCEMANAGER]
        self.assertRaises(
            SystemExit, self.call, sync_cmd.ResourceSync, app_args=[
                '--resources', FAKE_RESOURCE,
                '--source', FAKE_SOURCE_REGION,
                '--target', FAKE_TARGET_REGION])

    def test_resource_sync_without_source_region(self):
        self.client.sync_manager.sync_resources.\
            return_value = [SYNC_RESOURCEMANAGER]
        self.assertRaises(
            SystemExit, self.call, sync_cmd.ResourceSync, app_args=[
                '--resource_type', FAKE_RESOURCE_TYPE,
                '--resources', FAKE_RESOURCE,
                '--target', FAKE_TARGET_REGION])

    def test_resource_sync_without_target_region(self):
        self.client.sync_manager.sync_resources.\
            return_value = [SYNC_RESOURCEMANAGER]
        self.assertRaises(
            SystemExit, self.call, sync_cmd.ResourceSync, app_args=[
                '--resource_type', FAKE_RESOURCE_TYPE,
                '--resources', FAKE_RESOURCE,
                '--source', FAKE_SOURCE_REGION])

    def test_resource_sync_with_force(self):
        self.client.sync_manager.sync_resources.\
            return_value = [SYNC_RESOURCEMANAGER]
        actual_call = self.call(
            sync_cmd.ResourceSync, app_args=[
                '--resource_type', FAKE_RESOURCE_TYPE,
                '--resources', FAKE_RESOURCE,
                '--source', FAKE_SOURCE_REGION,
                '--target', FAKE_TARGET_REGION,
                '--force'])
        self.assertEqual([(ID, FAKE_STATUS, TIME_NOW)], actual_call[1])
