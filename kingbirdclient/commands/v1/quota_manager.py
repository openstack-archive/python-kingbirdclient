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

from osc_lib.command import command

from kingbirdclient.commands.v1 import base
from kingbirdclient import exceptions


def format(quotas=None):
    columns = (
        'Quota',
        'Limit'
    )

    if quotas:
        data = (
            quotas._data,
            quotas._Limit,
        )

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


def detailformat(quotas=None):
    columns = (
        'Quota',
        'Usage',
        'Limit',
    )

    if quotas:
        data = (
            quotas._data,
            quotas._Usage,
            quotas._Limit,
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
            help='Lists global limit of a specified tenant-id.'
                 ' Admin tenant can perform this operation.'
        )

        return parser

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        target_tenant_id = parsed_args.tenant
        return kingbird_client.quota_manager.global_limits(target_tenant_id)


class UpdateGlobalLimits(base.KingbirdLister):
    """Update the quotas for a tenant."""

    def _get_format_function(self):
        return format

    def get_parser(self, parsed_args):
        parser = super(UpdateGlobalLimits, self).get_parser(parsed_args)

        parser.add_argument(
            'tenant',
            help='ID of tenant to set the quotas .'
        )

        parser.add_argument(
            '--metadata_items',
            help='New value for the "metadata-items" quota'
        )

        parser.add_argument(
            '--subnet',
            help='New value for the "subnet" quota'
        )

        parser.add_argument(
            '--network',
            help='New value for the "network" quota'
        )

        parser.add_argument(
            '--floatingip',
            help='New value for the "floatingip" quota'
        )

        parser.add_argument(
            '--gigabytes',
            help='New value for the "gigabytes" quota'
        )

        parser.add_argument(
            '--backup_gigabytes',
            help='New value for the "backup_gigabytes" quota'
        )

        parser.add_argument(
            '--ram',
            help='New value for the "ram" quota'
        )

        parser.add_argument(
            '--floating_ips',
            help='New value for the "floating_ips" quota'
        )

        parser.add_argument(
            '--snapshots',
            help='New value for the "snapshots" quota'
        )

        parser.add_argument(
            '--security_group_rule',
            help='New value for the "security_group_rule" quota'
        )

        parser.add_argument(
            '--instances',
            help='New value for the "instances" quota'
        )

        parser.add_argument(
            '--key_pairs',
            help='New value for the "key_pairs" quota'
        )

        parser.add_argument(
            '--volumes',
            help='New value for the "volumes" quota'
        )

        parser.add_argument(
            '--router',
            help='New value for the "router" quota'
        )

        parser.add_argument(
            '--security_group',
            help='New value for the "security_group" quota'
        )

        parser.add_argument(
            '--cores',
            help='New value for the "cores" quota'
        )

        parser.add_argument(
            '--backups',
            help='New value for the "backups" quota'
        )

        parser.add_argument(
            '--fixed_ips',
            help='New value for the "fixed_ips" quota'
        )

        parser.add_argument(
            '--port',
            help='New value for the "port" quota'
        )

        parser.add_argument(
            '--security_groups',
            help='New value for the "security_groups" quota'
        )

        return parser

    def _get_resources(self, parsed_args):
        target_tenant_id = parsed_args.tenant
        kingbird_client = self.app.client_manager.sync_engine
        kwargs = {
            "metadata_items": parsed_args.metadata_items,
            "subnet": parsed_args.subnet,
            "network": parsed_args.network,
            "floatingip": parsed_args.floatingip,
            "gigabytes": parsed_args.gigabytes,
            "backup_gigabytes": parsed_args.backup_gigabytes,
            "ram": parsed_args.ram,
            "floating_ips": parsed_args.floating_ips,
            "snapshots": parsed_args.snapshots,
            "security_group_rule": parsed_args.security_group_rule,
            "instances": parsed_args.instances,
            "key_pairs": parsed_args.key_pairs,
            "volumes": parsed_args.volumes,
            "router": parsed_args.router,
            "security_group": parsed_args.security_group,
            "cores": parsed_args.cores,
            "backups": parsed_args.backups,
            "fixed_ips": parsed_args.fixed_ips,
            "port": parsed_args.port,
            "security_groups": parsed_args.security_groups
        }
        return kingbird_client.quota_manager.\
            update_global_limits(target_tenant_id, **kwargs)


class ShowQuotaDetail(base.KingbirdLister):
    """List the Detail limit for a tenant."""

    def _get_format_function(self):
        return detailformat

    def get_parser(self, parsed_args):
        parser = super(ShowQuotaDetail, self).get_parser(parsed_args)

        parser.add_argument(
            '--tenant',
            help='Lists global limit of a specified tenant-id.'
                 ' Admin tenant can perform this operation.'
        )

        return parser

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        target_tenant_id = parsed_args.tenant
        return kingbird_client.quota_manager.quota_detail(target_tenant_id)


class SyncQuota(command.Command):
    """On Demand quota sync for a tenant."""

    def get_parser(self, prog_name):
        parser = super(SyncQuota, self).get_parser(prog_name)

        parser.add_argument(
            'tenant',
            help='tenant-id to delete quotas.'
        )

        return parser

    def take_action(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        target_tenant = parsed_args.tenant
        try:
            kingbird_client.quota_manager.sync_quota(target_tenant)
            print("Request to sync quota for tenant %s has been triggered." %
                  (parsed_args.tenant))
        except Exception as e:
            print(e)
            error_msg = "Unable to sync quota for tenant %s." \
                        % (parsed_args.tenant)
            raise exceptions.KingbirdClientException(error_msg)


class DeleteQuota(command.Command):
    """Delete quota for a tenant."""

    def get_parser(self, prog_name):
        parser = super(DeleteQuota, self).get_parser(prog_name)

        parser.add_argument(
            'tenant',
            help='ID of tenant to delete quotas.'
        )

        return parser

    def take_action(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        target_tenant = parsed_args.tenant
        try:
            kingbird_client.quota_manager.\
                delete_quota(target_tenant)
            print("Request to delete quotas"
                  " for tenant %s has been accepted." %
                  (parsed_args.tenant))
        except Exception as e:
            print(e)
            error_msg = "Unable to delete quota for specified resource."
            raise exceptions.KingbirdClientException(error_msg)
