"""
MIT License
Copyright (c) 2016 Ionata Digital
Copyright (c) 2009-2014 Joshua Roesslein

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

from senaps_sensor.binder import bind_api
from senaps_sensor.error import SenapsError
from senaps_sensor.parsers import ModelParser, Parser
from senaps_sensor.utils import list_to_csv
from senaps_sensor.const import VALID_PROTOCOLS


class API(object):
    """Senaps API"""

    def __init__(self, auth_handler=None,
                 host='senaps.io', cache=None, api_root='/api/sensor/v2',
                 retry_count=0, retry_delay=0, retry_errors=None, timeout=60, parser=None,
                 compression=False, wait_on_rate_limit=False, connect_retries=3, read_retries=3,
                 backoff_factor=0.5, status_retries=3,
                 wait_on_rate_limit_notify=False, proxy='', verify=True, protocol='https'):
        """ Api instance Constructor

        :param auth_handler:
        :param host:  url of the server of the rest api, default:'senaps.io'
        :param cache: Cache to query if a GET method is used, default:None
        :param api_root: suffix of the api version, default:'/1.1'
        :param retry_count: number of allowed retries, default:0
        :param retry_delay: delay in second between retries, default:0
        :param retry_errors: default:None
        :param timeout: delay before to consider the request as timed out in seconds, default:60
        :param parser: ModelParser instance to parse the responses, default:None
        :param compression: If the response is compressed, default:False
        :param wait_on_rate_limit: If the api wait when it hits the rate limit, default:False
        :param wait_on_rate_limit_notify: If the api print a notification when the rate limit is hit, default:False
        :param proxy: Url to use as proxy during the HTTP request, default:''
        :param protocol: specify connection protocol to use. https by default.
        :param verify: Verify SSL certs if true. Will have no affect if protocol='http'
        :raise TypeError: If the given parser is not a ModelParser instance.
        :raise ValueError: If the given protocol is not in the set 'http', 'https'
        """
        self.auth = auth_handler
        self.protocol = protocol.lower()
        self.verify = verify
        self.host = host
        self.api_root = api_root
        self.cache = cache
        self.compression = compression
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.connect_retries = connect_retries
        self.read_retries = read_retries
        self.status_retries = status_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.wait_on_rate_limit = wait_on_rate_limit
        self.wait_on_rate_limit_notify = wait_on_rate_limit_notify
        self.parser = parser or ModelParser()
        self.proxy = {}

        if self.protocol not in VALID_PROTOCOLS:
            raise ValueError('"protocol" argument must be in %s' % (','.join(VALID_PROTOCOLS)))

        if proxy:
            self.proxy[self.protocol] = proxy

        parser_type = Parser
        if not isinstance(self.parser, parser_type):
            raise TypeError(
                '"parser" argument has to be an instance of "{required}".'
                ' It is currently a {actual}.'.format(
                    required=parser_type.__name__,
                    actual=type(self.parser)
                )
            )

    @property
    def me(self):
        """ Get the authenticated user using root api call
            :reference: https://senaps.io/api-docs/#/default/get_
            :allowed_param: 
        """
        res = bind_api(
            api=self,
            path='/',
            payload_type='json',
            allowed_param=[],
            require_auth=True,
        )
        return self.get_user(id=res()['_embedded']['user'][0]['id'])

    @property
    def users(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_users
            :allowed_param: 'id', 'roleids'
        """
        return bind_api(
            api=self,
            path='/users',
            payload_type='user',
            payload_list=True,
            query_only_param=[
                'id',
                'roleids'
            ],
            require_auth=True,
        )

    @property
    def get_user(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_users_userid
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            path='/users/{id}',
            payload_type='user',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def create_user(self):
        """ :reference: https://senaps.io/api-docs/#!/default/put_users_userid
            :allowed_param: 'id', 'hidden', 'roleids'
        """
        return bind_api(
            api=self,
            method='PUT',
            path='/users/{id}',
            payload_type='user',
            allowed_param=['id',
                           'hidden',
                           'roleids',
                           'eulaids'],
            require_auth=True,
        )

    @property
    def update_user(self):
        """ :reference: https://senaps.io/api-docs/#!/default/put_users_userid
            :allowed_param: 'id', 'hidden', 'roleids'
        """
        return bind_api(
            api=self,
            method='PUT',
            path='/users/{id}',
            payload_type='user',
            allowed_param=['id',
                           'hidden',
                           'roleids',
                           'eulaids'],
            require_auth=True,
        )

    @property
    def delete_user(self):
        """ :reference: https://senaps.io/api-docs/#!/default/delete_users_userid
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            method='DELETE',
            path='/users/{id}',
            payload_type='user',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def roles(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_roles
            :allowed_param: 'id', 'name', 'organisationid', 'groupids', 'streamids'
        """
        return bind_api(
            api=self,
            path='/roles',
            payload_type='role',
            payload_list=True,
            query_only_param=[
                'id',
                'type',
                'permissions',
                'organisationids',
                'groupids',
                'limit',
                'skip',
                'expand',
                'recursive',
                'usermetadatafield',
                'usermetadatavalues'
            ],
            require_auth=True,
        )

    @property
    def get_role(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_roles_roleid
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            method='GET',
            path='/roles/{id}',
            payload_type='role',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def create_role(self):
        """ :reference: https://senaps.io/api-docs/#!/default/put_roles_roleid
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            method='PUT',
            path='/roles/{id}',
            payload_type='role',
            allowed_param=[
                'id',
                'permissions',
                'type',
                'organisationid',
                'groupid',
                'addressfilters',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def update_role(self):
        """ :reference: https://senaps.io/api-docs/#!/default/put_roles_roleid
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            method='PUT',
            path='/roles/{id}',
            payload_type='role',
            allowed_param=[
                'id',
                'permissions',
                'type',
                'organisationid',
                'groupid',
                'addressfilters',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def delete_role(self):
        """ :reference: https://senaps.io/api-docs/#!/default/delete_roles_roleid
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            method='DELETE',
            path='/roles/{id}',
            payload_type='json',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def platforms(self):
        """ :reference: https://senaps.io/api-docs/#/default/platforms
            :allowed_param: 'id', 'name', 'organisationid', 'groupids', 'streamids'
        """
        return bind_api(
            api=self,
            path='/platforms',
            payload_type='platform',
            payload_list=True,
            query_only_param=[
                'id',
                'name',
                'organisationid',
                'groupids',
                'streamids',
                'usermetadatafield',
                'usermetadatavalues',
                'expand',
                'recursive',
            ],
            require_auth=True,
        )

    @property
    def create_platform(self):
        """ :reference: https://senaps.io/api-docs/#/default/put_platforms_id
            :allowed_param: 'id', 'name', 'organisationid', 'groupids', 'streamids', 'deployments'
        """
        return bind_api(
            api=self,
            path='/platforms/{id}',
            method='PUT',
            payload_type='platform',
            action='create',
            allowed_param=[
                'id',
                'name',
                'organisationid',
                'groupids',
                'streamids',
                'deployments',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def update_platform(self):
        """ :reference: https://senaps.io/api-docs/#/default/put_platforms_id
            :allowed_param: 'id', 'name', 'organisationid', 'groupids', 'streamids', 'deployments',
        """
        return bind_api(
            api=self,
            path='/platforms/{id}',
            method='PUT',
            payload_type='platform',
            action='update',
            allowed_param=[
                'id',
                'name',
                'organisationid',
                'groupids',
                'streamids',
                'deployments',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def destroy_platform(self):
        """ :reference: https://senaps.io/api-docs/#/default/delete_platforms_id
            :allowed_param: 'id', 'cascade'
        """
        return bind_api(
            api=self,
            path='/platforms/{id}',
            method='DELETE',
            payload_type='platform',
            allowed_param=[
                'id',
            ],
            query_only_param=[
                'cascade',
            ],
            require_auth=True,
        )

    @property
    def get_platform(self):
        """ :reference: https://senaps.io/api-docs/#/default/get_platform_id
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            path='/platforms/{id}',
            method='GET',
            payload_type='platform',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def streams(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_streams
            :allowed_param: 'id,limit'
        """
        return bind_api(
            api=self,
            path='/streams',
            payload_type='stream',
            allowed_param=['limit', 'id'],
            query_only_param=[
                'id',
                'limit',
                'skip',
                'near',
                'radius',
                'resulttype',
                'expand',
                'recursive',
                'groupids',
                'organisationid',
                'locationid',
                'usermetadatafield',
                'usermetadatavalues',
                'properties'
            ],
            payload_list=True,
            require_auth=True,
        )

    @property
    def locations(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_locations
            :allowed_param: 'id,limit'
        """
        return bind_api(
            api=self,
            path='/locations',
            payload_type='location',
            allowed_param=['id'],
            query_only_param=[
                'id',
                'description',
                'limit',
                'skip',
                'near',
                'radius',
                'expand',
                'groupids',
                'organisationid',
                'usermetadatafield',
                'usermetadatavalues',
            ],
            payload_list=True,
            require_auth=True,
        )

    @property
    def get_stream(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_streams_id
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            path='/streams/{id}',
            method='GET',
            payload_type='stream',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def create_stream(self):
        """ :reference: https://senaps.io/api-docs/#!/default/put_streams_id
            :allowed_param: 'id', 'resulttype', 'organisationid', 'groupids', 'procedureid', 'samplePeriod',
            'reportingPeriod', 'streamMetadata', 'locationid'
        """
        return bind_api(
            api=self,
            path='/streams/{id}',
            method='PUT',
            payload_type='stream',
            action='create',
            allowed_param=[
                'id',
                'resulttype',
                'organisationid',
                'groupids',
                'locationid',
                'procedureid',
                'samplePeriod',
                'reportingPeriod',
                'streamMetadata',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def update_stream(self):
        return self.create_stream

    @property
    def destroy_stream(self):
        """ :reference: https://senaps.io/api-docs/#!/default/delete_streams_id
            :allowed_param: 'id', 'cascade'
        """
        return bind_api(
            api=self,
            path='/streams/{id}',
            method='DELETE',
            payload_type='stream',
            allowed_param=[
                'id',
            ],
            query_only_param=[
                'cascade',
            ],
            require_auth=True,
        )

    @property
    def create_location(self):
        """ :reference: https://senaps.io/api-docs/#!/default/put_location_id
            :allowed_param: 'id', 'description', 'organisationid', 'geoJson'
        """
        return bind_api(
            api=self,
            path='/locations/{id}',
            method='PUT',
            payload_type='json',
            action='create',
            allowed_param=[
                'id',
                'organisationid',
                'description',
                'geoJson',
                'groupids',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def get_location(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_location_id
            :allowed_param: 'id'
        """
        return bind_api(
            api=self,
            path='/locations/{id}',
            method='GET',
            payload_type='location',
            allowed_param=['id'],
            require_auth=True,
        )

    @property
    def destroy_location(self):
        """ :reference: https://senaps.io/api-docs/#!/default/delete_locations_id
            :allowed_param: 'id', 'cascade'
        """
        return bind_api(
            api=self,
            path='/locations/{id}',
            method='DELETE',
            payload_type='location',
            allowed_param=[
                'id',
            ],
            query_only_param=[
                'cascade',
            ],
            require_auth=True,
        )

    @property
    def get_aggregation(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_aggregation
            :allowed_param: 'streamid', 'start', 'end', 'si', 'ei',
            'limit', 'aggperiod', 'count'
        """
        return bind_api(
            api=self,
            path='/aggregation',
            method='GET',
            payload_type='json',
            allowed_param=[
            ],
            query_only_param=[
                'streamid',
                'start',
                'end',
                'si',
                'ei',
                'limit',
                'aggperiod',
                'count',
            ],
            require_auth=True,
        )

    @property
    def create_observations(self):
        """ :reference: https://senaps.io/api-docs/#!/default/post_observations
            :allowed_param: 'streamid', 'results'
        """
        return bind_api(
            api=self,
            path='/observations',
            method='POST',
            payload_type='json',
            action='create',
            allowed_param=[
                'streamid',
                'results',
            ],
            query_only_param=[
                'streamid',
            ],
            require_auth=True,
        )

    @property
    def get_observations(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_observations
            :allowed_param: 'streamid', 'start', 'end', 'time', 'si', 'ei',
            'bounds', 'media', 'limit', 'sort'
        """
        return bind_api(
            api=self,
            path='/observations',
            method='GET',
            payload_type='json',
            allowed_param=[
            ],
            query_only_param=[
                'streamid',
                'start',
                'end',
                'time',
                'si',
                'ei',
                'bounds',
                'media',
                'limit',
                'sort',
            ],
            require_auth=True,
        )

    @property
    def destroy_observations(self):
        """ :reference: https://senaps.io/api-docs/#!/default/delete_observations
            :allowed_param: 'streamid'
        """
        return bind_api(
            api=self,
            path='/observations',
            method='DELETE',
            payload_type='json',
            query_only_param=[
                'streamid',
            ],
            require_auth=True,
        )

    @property
    def create_group(self):
        """ :reference:
        https://senaps.io/api-docs/#!/default/put_groups_id
            :allowed_param: 'id', 'name', 'organisationid', 'description', 'groupids'
        """
        return bind_api(
            api=self,
            path='/groups/{id}',
            method='PUT',
            payload_type='json',
            action='create',
            allowed_param=[
                'id',
                'name',
                'organisationid',
                'description',
                'groupids',
                'usermetadata',
            ],
            require_auth=True,
        )

    @property
    def get_groups(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_groups
            :allowed_param: 'id', 'organisationid', 'groupids', 'limit', 'skip', 'expand', 'recursive'
        """
        return bind_api(
            api=self,
            path='/groups',
            method='GET',
            payload_type='group',
            payload_list=True,
            allowed_param=[
            ],
            query_only_param=[
                'id',
                'organisationid',
                'groupids',
                'limit',
                'skip',
                'expand',
                'recursive',
                'usermetadatafield',
                'usermetadatavalues',
            ],
            require_auth=True,
        )

    @property
    def destroy_group(self):
        """ :reference: https://senaps.io/api-docs/#!/default/delete_group
            :allowed_param: 'id', 'cascade'
        """
        return bind_api(
            api=self,
            path='/groups/{id}',
            method='DELETE',
            payload_type='group',
            allowed_param=[
                'id',
            ],
            query_only_param=[
                'cascade',
            ],
            require_auth=True,
        )

    @property
    def get_group(self):
        """ :reference: https://senaps.io/api-docs/#!/default/get_group
            :allowed_param: 'id', 'recursive'
        """
        return bind_api(
            api=self,
            path='/groups/{id}',
            method='GET',
            payload_type='json',
            allowed_param=['id', 'recursive'],
            require_auth=True,
        )

    @property
    def get_permitted(self):
        """
        Currently no public documentation for this item.
        This endpoint is used to verify whether the current user is permitted to
        access the specified resources.
        :allowed_param: 'permission', 'resourceid', 'organisationid', 'groupids'
        :return:
        """
        return bind_api(
            api=self,
            path='/permitted',
            method='GET',
            payload_type='permitted',
            allowed_param=[],
            query_only_param=[
                'permission',
                'resourceid',
                'organisationid',
                'groupids'
            ],
            require_auth=True
        )
