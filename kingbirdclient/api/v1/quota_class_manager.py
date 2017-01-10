# Copyright (c) 2017 Ericsson AB.
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


class QuotaClass(base.Resource):
    resource_name = 'os-quota-class-sets'

    def __init__(self, manager, data, Limit):
        self.manager = manager
        self._data = data
        self._Limit = Limit


class quota_class_manager(base.ResourceManager):
    resource_class = QuotaClass

    def list_quota_class(self, quota_class):
        tenant = self.http_client.project_id
        url = '/%s/os-quota-class-sets/%s' % (tenant, quota_class)
        return self._list(url)

    def quota_class_update(self, quota_class, **kwargs):
        if kwargs:
            data = dict()
            data['quota_class_set'] = {
                k: int(v) for k, v in kwargs.items() if v is not None}
        tenant = self.http_client.project_id
        url = '/%s/os-quota-class-sets/%s' % (tenant, quota_class)
        return self._update(url, data)

    def delete_quota_class(self, quota_class):
        tenant = self.http_client.project_id
        url = '/%s/os-quota-class-sets/%s' % (tenant, quota_class)
        return self._delete(url)
