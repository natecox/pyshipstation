import unittest
from nose.tools import raises
from shipstation.api import *


class ShipStationAddressTest(unittest.TestCase):
    def test_address_init_works(self):
        self.json = {
            'name': 'Joe Smith',
            'company': 'Widgets Inc',
            'street1': '123 Main St',
            'street2': 'Building 1',
            'street3': 'Ste 101',
            'city': 'Big City',
            'state': 'AK',
            'postal_code': '12345',
            'country': 'US',
            'residential': True,
            'phone': '123-456-7890'
        }

        self.ss_address = ShipStationAddress(**self.json)

        self.assertDictEqual(self.ss_address.__dict__, self.json)

    @raises(AttributeError)
    def test_address_residential_is_bool_or_empty(self):
        ShipStationAddress(
            name='some name',
            residential='something'
        )

    @raises(AttributeError)
    def test_address_must_have_name(self):
        ShipStationAddress(
            name=''
        )

    @raises(AttributeError)
    def test_address_country_must_be_two_letters(self):
        ShipStationAddress(
            name='some name',
            country='country'
        )
