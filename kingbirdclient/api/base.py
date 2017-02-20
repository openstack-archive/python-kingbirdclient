# Copyright (c) 2016 Ericsson AB
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

import json

from kingbirdclient import exceptions


class Resource(object):
    # This will be overridden by the actual resource
    resource_name = 'Something'


class ResourceManager(object):
    resource_class = None

    def __init__(self, http_client):
        self.http_client = http_client

    def _generate_resource(self, json_response_key):
        json_objects = [json_response_key[item] for item in json_response_key]
        resource = []
        for json_object in json_objects:
            for resource_data in json_object:
                resource.append(self.resource_class(self, resource_data,
                                json_object[resource_data]))
        return resource

    def _list(self, url, response_key=None):
        resp = self.http_client.get(url)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        resource = self._generate_resource(json_response_key)
        return resource

    def _update(self, url, data):
        data = json.dumps(data)
        resp = self.http_client.put(url, data)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        result = self._generate_resource(json_response_key)
        return result

    def _sync(self, url, data=None):
        resp = self.http_client.put(url, data)
        if resp.status_code != 200:
            self._raise_api_exception(resp)

    def _detail(self, url):
        resp = self.http_client.get(url)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        json_objects = [json_response_key[item] for item in json_response_key]
        resource = []
        for json_object in json_objects:
            data = json_object.get('usage').keys()
            for values in data:
                resource.append(self.resource_class(self, values,
                                json_object['limits'][values],
                                json_object['usage'][values]))
        return resource

    def resource_sync_create(self, url, data):
        data = json.dumps(data)
        resp = self.http_client.post(url, data)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        json_object = json_response_key['job_status']
        resource = []
        resource.append(self.resource_class(
                        self, id=json_object['id'],
                        status=json_object['status'],
                        created_at=json_object['created_at']))
        return resource

    def _resource_sync_list(self, url):
        resp = self.http_client.get(url)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        json_objects = json_response_key['job_set']
        resource = []
        for json_object in json_objects:
            resource.append(self.resource_class(
                            self, id=json_object['id'],
                            status=json_object['sync_status'],
                            created_at=json_object['created_at'],
                            updated_at=json_object['updated_at']))
        return resource

    def _resource_sync_detail(self, url):
        resp = self.http_client.get(url)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        json_objects = json_response_key['job_set']
        resource = []
        for json_object in json_objects:
            resource.append(self.resource_class(
                            self, resource_name=json_object['resource'],
                            source_region=json_object['source_region'],
                            target_region=json_object['target_region'],
                            resource_type=json_object['resource_type'],
                            status=json_object['sync_status'],
                            created_at=json_object['created_at'],
                            updated_at=json_object['updated_at']))
        return resource

    def _delete(self, url):
        resp = self.http_client.delete(url)
        if resp.status_code != 200:
            self._raise_api_exception(resp)

    def _raise_api_exception(self, resp):
        error_data = resp.content
        raise exceptions.APIException(error_code=resp.status_code,
                                      error_message=error_data)


def get_json(response):
    """Get JSON representation of response."""
    json_field_or_function = getattr(response, 'json', None)
    if callable(json_field_or_function):
        return response.json()
    else:
        return json.loads(response.content)
