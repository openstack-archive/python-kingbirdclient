# Copyright 2016 Ericsson AB
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


class KingbirdClientException(Exception):
    """Base Exception for Kingbird client

    To correctly use this class, inherit from it and define
    a 'message' and 'code' properties.
    """
    message = "An unknown exception occurred"
    code = "UNKNOWN_EXCEPTION"

    def __str__(self):
        return self.message

    def __init__(self, message=message):
        self.message = message
        super(KingbirdClientException, self).__init__(
            '%s: %s' % (self.code, self.message))


class IllegalArgumentException(KingbirdClientException):
    message = "IllegalArgumentException occurred"
    code = "ILLEGAL_ARGUMENT_EXCEPTION"

    def __init__(self, message=None):
        if message:
            self.message = message


class CommandError(KingbirdClientException):
    message = "CommandErrorException occurred"
    code = "COMMAND_ERROR_EXCEPTION"

    def __init__(self, message=None):
        if message:
            self.message = message


class APIException(Exception):
    def __init__(self, error_code=None, error_message=None):
        super(APIException, self).__init__(error_message)
        self.error_code = error_code
        self.error_message = error_message
