# Copyright 2016 Ericsson AB.
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

import re

from testtools import matchers

from kingbirdclient.tests import base_shell_test as base


class TestCLIBashCompletionV1(base.BaseShellTests):
    def test_bash_completion(self):
        bash_completion, stderr = self.shell('bash-completion')
        self.assertIn('bash-completion', bash_completion)
        self.assertFalse(stderr)


class TestCLIHelp(base.BaseShellTests):
    def test_help(self):
        required = [
            '.*?^usage: ',
            '.*?^\s+help\s+print detailed help for another command'
            ]
        kb_help, stderr = self.shell('help')
        for r in required:
            self.assertThat((kb_help + stderr),
                            matchers.MatchesRegex(r, re.DOTALL | re.MULTILINE))
