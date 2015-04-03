from django.conf import settings
import requests

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

    def get(self, endpoint):
        url = '{}{}'.format(self.url, endpoint)
        r = requests.get(url, auth=(self.key, self.secret))
        print r.json()
