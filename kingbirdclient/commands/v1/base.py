# Copyright (c) 2016 Ericsson AB
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import abc

from osc_lib.command import command
import six


@six.add_metaclass(abc.ABCMeta)
class KingbirdLister(command.Lister):
    @abc.abstractmethod
    def _get_format_function(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_resources(self, parsed_args):
        """Get a list of API resources (e.g. using client)."""
        raise NotImplementedError

    def _validate_parsed_args(self, parsed_args):
        # No-op by default.
        pass

    def take_action(self, parsed_args):
        self._validate_parsed_args(parsed_args)
        f = self._get_format_function()

        ret = self._get_resources(parsed_args)
        if not isinstance(ret, list):
            ret = [ret]

        data = [f(r)[1] for r in ret]

        if data:
            return f()[0], data
        else:
            return f()
