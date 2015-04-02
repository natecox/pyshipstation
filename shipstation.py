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
            raise AttributeError('Key must be supplied.')
        else:
            self.key = key

        if secret is None:
            raise AttributeError('Secret must be supplied.')
        else:
            self.secret = secret

    def get(self, endpoint):
        url = '{}/{}'.format(self.url, endpoint)
        r = requests.get(url, auth=(self.secret, self.key))
        print r
