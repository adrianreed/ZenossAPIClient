# -*- coding: utf-8 -*-

"""
Zenoss API Client Class
"""

import inspect
import os
import urllib3


class ZenossAPIClientError(Exception):
    pass


class ZenossAPIClientAuthenticationError(Exception):
    pass


class Client(object):
    """Client class to access the Zenoss JSON API"""

    def __init__(self, host=None, user=None, password=None, ssl_verify=True):
        """
        Create the client object to communicate with Zenoss

        Arguments:
            host (str): FQDN used to access the Zenoss server
            user (str): Zenoss username
            password (str): Zenoss user's password

        """
        if not host:
            if 'ZENOSS_HOST' in os.environ:
                host = os.environ['ZENOSS_HOST']
        if not user:
            if 'ZENOSS_USER' in os.environ:
                user = os.environ['ZENOSS_USER']
        if not password:
            if 'ZENOSS_PASSWD' in os.environ:
                password = os.environ['ZENOSS_PASSWD']

        self.api_host = host
        self.api_url = 'https://{0}/zport/dmd'.format(host)
        self.api_user = user
        self.ssl_verify = ssl_verify
        self.api_headers = {"Content-Type": "application/json"}
        self.router_list = []
        self.routers = dict()

        for router in self.get_routers():
            self.router_list.append(router)
            self.routers[router] = __import__(
                'zenossapi.routers.{0}'.format(router),
                fromlist=[router])

        if self.api_user and password:
            self.api_headers.update(urllib3.make_headers(
                basic_auth='{0}:{1}'.format(self.api_user, password)))

    def get_routers(self):
        """
        Gets the list of availble Zenoss API routers

        Returns:
            list:
        """
        router_list = []
        routers_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'routers')
        file_list = os.listdir(routers_path)
        for fname in file_list:
            name, ext = fname.split('.')
            if name == "__init__":
                continue
            if ext == "py":
                router_list.append(name)

        return router_list

    def get_router(self, router):
        """
        Instantiates and returns a Zenoss router object

        Arguments:
            router (str): The API router to use
        """
        api_router = getattr(
            self.routers[router],
            '{0}Router'.format(router.capitalize()),
        )(
            self.api_url,
            self.api_headers,
            self.ssl_verify,
        )

        return api_router

    def get_router_methods(self, router):
        """
        List all available methods for an API router

        Arguments:
            router (str): The router to get methods from

        Returns:
            list:
        """
        router_methods = []
        for method in inspect.getmembers(
            getattr(self.routers[router],
                    '{0}Router'.format(router.capitalize())),
            predicate=inspect.isroutine
        ):
            if method[0].startswith('__'):
                continue
            router_methods.append(method[0])

        return router_methods