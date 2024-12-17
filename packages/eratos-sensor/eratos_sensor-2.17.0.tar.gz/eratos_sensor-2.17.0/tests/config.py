"""
MIT License
Copyright (c) 2016 Ionata Digital

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import unicode_literals, absolute_import, print_function

from senaps_sensor.api import API

import vcr
import os
import six
from distutils.util import strtobool

from senaps_sensor.auth import HTTPBasicAuth, HTTPKeyAuth, HTTPConsumerIDAuth

if six.PY3:
    import unittest
else:
    import unittest2 as unittest

username = os.environ.get('SENAPS_USERNAME', 'username')
password = os.environ.get('SENAPS_PASSWORD', 'password')
api_key = os.environ.get('SENAPS_APIKEY')
host = os.environ.get('API_BASE', 'senaps.io')
ssl_verify = bool(strtobool(os.environ.get('SSL_VERIFY', "True")))
use_replay = bool(strtobool(os.environ.get('USE_REPLAY', "0")))


tape = vcr.VCR(
    cassette_library_dir='cassettes',
    filter_headers=['Authorization', 'apikey'],
    filter_query_parameters=['apikey'],
    serializer='json',
    # Either use existing cassettes, or never use recordings:
    record_mode='none' if use_replay else 'all',
)


class SensorApiTestCase(unittest.TestCase):
    def setUp(self):
        if api_key is None:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = HTTPKeyAuth(api_key)

        self.api = API(self.auth, host=host, verify=ssl_verify)
        self.api.retry_count = 0
        self.api.retry_delay = 5


class SensorApiInternalTestCase(unittest.TestCase):
    def setUp(self):
        self.auth = HTTPConsumerIDAuth(username)

        self.api = API(self.auth, host=host, verify=ssl_verify)
        self.api.retry_count = 0
        self.api.retry_delay = 5
