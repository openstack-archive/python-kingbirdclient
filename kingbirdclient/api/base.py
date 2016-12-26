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


class Resource(object):
    # This will be overridden by the actual resource
    resource_name = 'Something'

    def __init__(self, manager, data, values):
        self.manager = manager
        self._data = data
        self._values = values


class ResourceManager(object):
    resource_class = None

    def __init__(self, http_client):
        self.http_client = http_client

    def _list(self, url, response_key=None):
        resp = self.http_client.get(url)
        if resp.status_code != 200:
            self._raise_api_exception(resp)
        json_response_key = get_json(resp)
        json_objects = [json_response_key[item] for item in json_response_key]

        resource = []
        for json_object in json_objects:
            for resource_data in json_object:
                resource.append(self.resource_class(self, resource_data,
                                json_object[resource_data]))
        return resource


def get_json(response):
    """Get JSON representation of response."""
    json_field_or_function = getattr(response, 'json', None)
    if callable(json_field_or_function):
        if 'project_id' in response.json()['quota_set']:
            response = response.json()
            response['quota_set'].pop('project_id')
            return response
        return response.json()
    else:
        return json.loads(response.content)
