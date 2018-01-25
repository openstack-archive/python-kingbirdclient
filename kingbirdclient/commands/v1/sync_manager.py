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

import json
import yaml

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
        'ID',
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
            resources.id,
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


def sync_format(resources=None):
    columns = (
        'ID',
        'STATUS',
        'CREATED_AT',
    )

    if resources:
        data = (
            resources.id,
            resources.status,
            resources.created_at,
        )

    else:
        data = (tuple('<none>' for _ in range(len(columns))),)

    return columns, data


class ResourceSync(base.KingbirdLister):
    """Sync Resources from One region to other."""

    def _get_format_function(self):
        return sync_format

    def get_parser(self, parsed_args):
        parser = super(ResourceSync, self).get_parser(parsed_args)

        parser.add_argument(
            '--source',
            required=True,
            help='Source Region from which resources have to be synced.'
        )

        parser.add_argument(
            '--target',
            action='append',
            required=True,
            help='Target Region to which resources have to be synced.'
        )

        parser.add_argument(
            '--resource_type',
            required=True,
            help='Type of the resource to be synced.'
        )

        parser.add_argument(
            '--resources',
            action='append',
            required=True,
            help='Identifier of the resource',
        )

        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrites existing resources on the target regions.'
        )

        return parser

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        kwargs = dict()
        kwargs['resource_type'] = parsed_args.resource_type
        kwargs['force'] = str(parsed_args.force)
        kwargs['resources'] = parsed_args.resources
        kwargs['source'] = parsed_args.source
        kwargs['target'] = parsed_args.target
        return kingbird_client.sync_manager.sync_resources(**kwargs)


class TemplateResourceSync(base.KingbirdLister):
    """Sync multiple resource-types to multiple regions."""

    def _get_format_function(self):
        return sync_format

    def get_parser(self, parsed_args):
        parser = super(TemplateResourceSync, self).get_parser(parsed_args)

        parser.add_argument(
            'template',
            help='Specify the name of an input file in .yaml/.yml/.json.'
        )

        return parser

    def _get_resources(self, parsed_args):
        kingbird_client = self.app.client_manager.sync_engine
        kwargs = dict()
        sync_template = parsed_args.template
        try:
            with open(sync_template) as template_data:
                if sync_template.endswith('.yaml') or sync_template.endswith('.yml') \
                        or sync_template.endswith('.json'):
                    try:
                        if sync_template.endswith('.json'):
                            data = json.load(template_data)
                        else:
                            data = yaml.load(template_data)
                    except Exception:
                        raise exceptions.TemplateError(
                            'Syntactical errors in the template')
                else:
                    raise exceptions.TemplateError(
                        'Invalid extension.Provide .yaml/.yml/.json template')
            for iteration in data['Sync']:
                if 'source' not in iteration:
                    raise exceptions.TemplateError(
                        'source_region parameter is missing in template')
                if not iteration['source']:
                    raise exceptions.TemplateError(
                        'source_region parameter value is missing')
                if 'target' not in iteration:
                    raise exceptions.TemplateError(
                        'target_region parameter is missing in template')
                if not iteration['target']:
                    raise exceptions.TemplateError(
                        'target_region parameter value is missing')
                if 'resource_type' not in iteration:
                    raise exceptions.TemplateError(
                        'resource_type parameter is missing in template')
                if not iteration['resource_type']:
                    raise exceptions.TemplateError(
                        'resource_type parameter value is missing')
                if 'resources' not in iteration:
                    raise exceptions.TemplateError(
                        'resources parameter is missing in template')
                if not iteration['resources']:
                    raise exceptions.TemplateError(
                        'resources parameter value is missing')
        except Exception:
            raise
        kwargs.update(data)
        return kingbird_client.sync_manager.sync_resources(**kwargs)


class SyncList(base.KingbirdLister):
    """List Sync Jobs."""

    def _get_format_function(self):
        return format

    def get_parser(self, parsed_args):
        parser = super(SyncList, self).get_parser(parsed_args)

        parser.add_argument(
            '--active',
            action='store_true',
            help='View the list of active jobs.'
        )

        return parser

    def _get_resources(self, parsed_args):
        active = parsed_args.active
        action = None
        kingbird_client = self.app.client_manager.sync_engine
        if active:
            action = 'active'
        return kingbird_client.sync_manager.list_sync_jobs(action)


class SyncShow(base.KingbirdLister):
    """List the details of a Sync Job."""

    def _get_format_function(self):
        return detail_format

    def get_parser(self, parsed_args):
        parser = super(SyncShow, self).get_parser(parsed_args)

        parser.add_argument(
            'job_id',
            help='ID of the job to view the details.'
        )

        return parser

    def _get_resources(self, parsed_args):
        job = parsed_args.job_id
        kingbird_client = self.app.client_manager.sync_engine
        return kingbird_client.sync_manager.sync_job_detail(job)


class SyncDelete(command.Command):
    """Delete Sync Job(s) details from the database."""

    def get_parser(self, prog_name):
        parser = super(SyncDelete, self).get_parser(prog_name)

        parser.add_argument(
            'job_id',
            nargs="+",
            help='ID of the job to delete entries in database.'
        )

        return parser

    def take_action(self, parsed_args):
        jobs = parsed_args.job_id
        kingbird_client = self.app.client_manager.sync_engine
        for job in jobs:
            try:
                kingbird_client.sync_manager.delete_sync_job(job)
            except Exception as e:
                print (e)
                error_msg = "Unable to delete the entries of %s" % (job)
                raise exceptions.KingbirdClientException(error_msg)
