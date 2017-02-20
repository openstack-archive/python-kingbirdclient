# Copyright (c) 2017 Ericsson AB.
# All Rights Reserved.
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

from kingbirdclient.api import base


class Resource(base.Resource):
    resource_name = 'os-sync'

    def __init__(self, manager, status, created_at, updated_at,
                 resource_type=None, target_region=None,
                 source_region=None, id=None, resource_name=None,):
        self.manager = manager
        self._id = id
        self._source_region = source_region
        self._target_region = target_region
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at
        self._resource_name = resource_name
        self._resource_type = resource_type


class sync_manager(base.ResourceManager):
    resource_class = Resource

    def list_sync_jobs(self):
        tenant = self.http_client.project_id
        url = '/%s/os-sync/' % tenant
        return self._resource_sync_list(url)

    def sync_job_detail(self, job_id):
        tenant = self.http_client.project_id
        url = '/%s/os-sync/%s' % (tenant, job_id)
        return self._resource_sync_detail(url)

    def delete_sync_job(self, job_id):
        tenant = self.http_client.project_id
        url = '/%s/os-sync/%s' % (tenant, job_id)
        return self._delete(url)
