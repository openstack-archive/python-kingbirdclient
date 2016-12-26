# Copyright (c) 2016 Ericsson AB.
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

from kingbirdclient.commands.v1 import base


def format(quotas=None):
    columns = (
        'Quota',
        'Limit'
    )

    if quotas:
        data = (
            quotas._data,
            quotas._values,
        )

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class ListDefaults(base.KingbirdLister):
    """List all default quotas."""

    def _get_format_function(self):
        return format

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        return kingbird_client.quota_manager.list_defaults()


class GlobalLimits(base.KingbirdLister):
    """Lists the global limit of a tenant."""

    def _get_format_function(self):
        return format

    def get_parser(self, parsed_args):
        parser = super(GlobalLimits, self).get_parser(parsed_args)

        parser.add_argument(
            '--tenant',
            help='Lists global limit of a specified tenant (Admin only).'
        )

        return parser

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        target_tenant_id = parsed_args.tenant
        return kingbird_client.quota_manager.global_limits(target_tenant_id)
