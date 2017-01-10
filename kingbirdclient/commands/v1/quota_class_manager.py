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


class ListQuotaClass(base.KingbirdLister):
    """List the quotas for a quota class."""

    def _get_format_function(self):
        return format

    def get_parser(self, parsed_args):
        parser = super(ListQuotaClass, self).get_parser(parsed_args)
        parser.add_argument(
            'quota_class',
            help='Name of quota class to list the quotas.'
        )
        return parser

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        quota_class = parsed_args.quota_class
        return kingbird_client.quota_class_manager.\
            list_quota_class(quota_class)


class UpdateQuotaClass(base.KingbirdLister):
    """Update quotas for a quota class."""

    def _get_format_function(self):
        return format

    def get_parser(self, parsed_args):
        parser = super(UpdateQuotaClass, self).get_parser(parsed_args)

        parser.add_argument(
            'quota_class',
            help='Name of quota class to update the quotas.'
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
        quota_class = parsed_args.quota_class
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
        return kingbird_client.quota_class_manager.\
            quota_class_update(quota_class, **kwargs)


class DeleteQuotaClass(command.Command):
    """Delete quotas for a quota-class."""

    def get_parser(self, prog_name):
        parser = super(DeleteQuotaClass, self).get_parser(prog_name)

        parser.add_argument(
            'quota_class',
            help='Name of quota class to delete quotas.'
        )

        return parser

    def take_action(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        quota_class = parsed_args.quota_class
        try:
            kingbird_client.quota_class_manager.\
                delete_quota_class(quota_class)
            print("Request to delete %s quota_class has been accepted." %
                  (parsed_args.quota_class))
        except Exception as e:
            print(e)

            error_msg = "Unable to delete the specified quota_class."
            raise exceptions.KingbirdClientException(error_msg)
