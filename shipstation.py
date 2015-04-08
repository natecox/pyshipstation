from django.conf import settings
import requests


class ShipStationOrder:
    """
    Accepts the data needed for an individual ShipStation order and
    contains the tools for submitting the order to ShipStation.
    """

    def __init__(self):
        self.items = []
        self.container = None

    def add_item(self, key=None, sku=None, name=None, image_url=None,
                 weight=None, quantity=None, unit_price=None,
                 warehouse_location=None, options=None):
        """
        Adds a new item to the order with all of the required keys.
        """
        details = locals()
        details.pop('self')
        self.items.append(details)

    def get_items(self):
        return self.items


class ShipStation:
    """
    Handles the details of connecting to and querying a ShipStation account.
    """

    def __init__(self, key=None, secret=None):
        """
        Connecting to ShipStation required an account and a
        :return:
        """

        self.url = 'https://ssapi.shipstation.com'

        if key is None:
            self.key = settings.SHIPSTATION_SETTINGS.get('key')
            if self.key is None:
                raise AttributeError('Key must be supplied.')
        else:
            self.key = key

        if secret is None:
            self.secret = settings.SHIPSTATION_SETTINGS.get('secret')
            if self.key is None:
                raise AttributeError('Key must be supplied.')
        else:
            self.secret = secret

        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_orders(self):
        return self.orders

    def get(self, endpoint):
        url = '{}{}'.format(self.url, endpoint)
        r = requests.get(url, auth=(self.key, self.secret))
        print r.json()
