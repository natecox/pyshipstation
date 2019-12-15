import datetime
from decimal import Decimal
import json
import pprint
import requests
from shipstation.models import *
from shipstation.constants import *


class ShipStation(ShipStationBase):
    """
    Handles the details of connecting to and querying a ShipStation account.
    """

    def __init__(self, key=None, secret=None, debug=False):
        """
        Connecting to ShipStation required an account and a
        :return:
        """

        if key is None:
            raise AttributeError("Key must be supplied.")
        if secret is None:
            raise AttributeError("Secret must be supplied.")

        self.url = "https://ssapi.shipstation.com"

        self.key = key
        self.secret = secret
        self.orders = []
        self.timeout = 1.0
        self.debug = debug

    def add_order(self, order):
        self.require_type(order, ShipStationOrder)
        self.orders.append(order)

    def get_orders(self):
        return self.orders

    def submit_orders(self):
        for order in self.orders:
            self.post(endpoint="/orders/createorder", data=json.dumps(order.as_dict()))

    def get(self, endpoint="", payload=None):
        url = "{}{}".format(self.url, endpoint)
        r = requests.get(
            url, auth=(self.key, self.secret), params=payload, timeout=self.timeout
        )
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())

        return r

    def post(self, endpoint="", data=None):
        url = "{}{}".format(self.url, endpoint)
        headers = {"content-type": "application/json"}
        r = requests.post(
            url,
            auth=(self.key, self.secret),
            data=data,
            headers=headers,
            timeout=self.timeout,
        )
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())

        return r

    def put(self, endpoint="", data=None):
        url = "{}{}".format(self.url, endpoint)
        headers = {"content-type": "application/json"}
        r = requests.put(
            url,
            auth=(self.key, self.secret),
            data=data,
            headers=headers,
            timeout=self.timeout,
        )
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())

        return r

    def fetch_orders(self, parameters={}):
        """
            Query, fetch, and return existing orders from ShipStation

            Args:
                parameters (dict): Dict of filters to filter by.

            Raises:
                AttributeError: parameters not of type dict
                AttributeError: invalid key in parameters dict.

            Returns:
                A <Response [code]> object.

            Examples:
                >>> ss.fetch_orders(parameters={'order_status': 'shipped', 'page': '2'})
        """
        self.require_type(parameters, dict)
        invalid_keys = set(parameters.keys()).difference(ORDER_LIST_PARAMETERS)
        if invalid_keys:
            raise AttributeError(
                "Invalid order list parameters: {}".format(", ".join(invalid_keys))
            )

        valid_parameters = {
            self.to_camel_case(key): value for key, value in parameters.items()
        }

        return self.get(endpoint="/orders/list", payload=valid_parameters)
