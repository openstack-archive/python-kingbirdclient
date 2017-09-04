#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""OpenStackClient plugin for Sync service."""

import logging

from osc_lib import utils

LOG = logging.getLogger(__name__)

DEFAULT_SYNC_API_VERSION = '1'
API_VERSION_OPTION = 'os_sync_api_version'
API_NAME = 'sync_engine'
API_VERSIONS = {
    '1': 'kingbirdclient.api.v1.client.Client',
}


def make_client(instance):
    """Return a sync_engine service client."""
    version = instance._api_version[API_NAME]
    sync_client = utils.get_client_class(
        API_NAME,
        version,
        API_VERSIONS)

    LOG.debug('Instantiating sync engine client: %s', sync_client)

    kingbird_url = instance.get_endpoint_for_service_type(
        'synchronization',
        interface='publicURL'
    )

    client = sync_client(kingbird_url=kingbird_url, session=instance.session)

    return client


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-sync-api-version',
        metavar='<sync-api-version>',
        default=utils.env(
            'OS_SYNC_API_VERSION',
            default=DEFAULT_SYNC_API_VERSION),
        help='SYNC API version, default=' +
             DEFAULT_SYNC_API_VERSION +
             ' (Env: OS_SYNC_API_VERSION)')

    return parser
