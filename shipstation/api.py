import json
import requests
import pprint

from shipstation.data.order import ShipStationOrder


class ShipStation:
    """
    Handles the details of connecting to and querying a ShipStation account.
    """

    def __init__(self, key=None, secret=None, debug=False):
        """
        Connecting to ShipStation required an account and a
        :return:
        """

        if key is None:
            raise AttributeError('Key must be supplied.')
        if secret is None:
            raise AttributeError('Secret must be supplied.')

        self.url = 'https://ssapi.shipstation.com'

        self.key = key
        self.secret = secret
        self.orders = []

        self.debug = debug

    def add_order(self, order):
        if type(order) is not ShipStationOrder:
            raise AttributeError('Should be type ShipStationOrder')
        self.orders.append(order)

    def get_orders(self):
        return self.orders

    def submit_orders(self):
        for order in self.orders:
            self.post(
                endpoint='/orders/createorder',
                data=json.dumps(order.as_dict())
            )

    def get(self, endpoint=''):
        url = '{}{}'.format(self.url, endpoint)
        r = requests.get(url, auth=(self.key, self.secret))
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())

    def post(self, endpoint='', data=None):
        url = '{}{}'.format(self.url, endpoint)
        headers = {'content-type': 'application/json'}
        r = requests.post(
            url,
            auth=(self.key, self.secret),
            data=data,
            headers=headers
        )
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())
