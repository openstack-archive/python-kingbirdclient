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


def format(resources=None):
    columns = (
        'ID',
        'STATUS',
        'CREATED_AT',
        'UPDATED_AT',
    )

    if resources:
        data = (
            resources.id,
            resources.status,
            resources.created_at,
            resources.updated_at,
        )

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


def detail_format(resources=None):
    columns = (
        'RESOURCE',
        'SOURCE_REGION',
        'TARGET_REGION',
        'RESOURCE_TYPE',
        'STATUS',
        'CREATED_AT',
        'UPDATED_AT',
    )

    if resources:
        data = (
            resources.resource_name,
            resources.source_region,
            resources.target_region,
            resources.resource_type,
            resources.status,
            resources.created_at,
            resources.updated_at,
        )

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class SyncList(base.KingbirdLister):
    """List Sync Jobs."""

    def _get_format_function(self):
        return format

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        return kingbird_client.sync_manager.list_sync_jobs()


class SyncShow(base.KingbirdLister):
    """List the details of a Sync Job."""

    def _get_format_function(self):
        return detail_format

    def get_parser(self, parsed_args):
        parser = super(SyncShow, self).get_parser(parsed_args)

        parser.add_argument(
            'job_id',
            help='ID of Job to view the details.'
        )

        return parser

    def _get_resources(self, parsed_args):
        job_id = parsed_args.job_id
        kingbird_client = self.app.client_manager.sync_engine
        return kingbird_client.sync_manager.sync_job_detail(job_id)


class SyncDelete(command.Command):
    """Delete the Sync Job details from the database."""

    def get_parser(self, prog_name):
        parser = super(SyncDelete, self).get_parser(prog_name)

        parser.add_argument(
            'job_id',
            help='ID of the job to delete entries in database.'
        )

        return parser

    def take_action(self, parsed_args):
        job_id = parsed_args.job_id
        kingbird_client = self.app.client_manager.sync_engine
        try:
            kingbird_client.sync_manager.delete_sync_job(job_id)
            print("Request to delete %s 's entries has been accepted."
                  % (job_id))
        except Exception as e:
            print (e)
            error_msg = "Unable to delete the entries of the specified job"
            raise exceptions.KingbirdClientException(error_msg)
