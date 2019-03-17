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
            'phone': '123-456-7890',
            'residential': True
        }

        self.ss_address = ShipStationAddress(**self.json)

        self.assertEqual(json.dumps(self.ss_address.__dict__), json.dumps(self.json))

    @raises(AttributeError)
    def test_address_must_have_street1(self):
        ShipStationAddress(
            street1='',
            city='some city',
            state='some state',
            postal_code='some zip'
        )

    @raises(AttributeError)
    def test_address_must_have_city(self):
        ShipStationAddress(
            street1='123 main st',
            city='',
            state='some state',
            postal_code='some zip'
        )

    @raises(AttributeError)
    def test_address_must_have_state(self):
        ShipStationAddress(
            street1='123 main st',
            city='some city',
            state='',
            postal_code='some zip'
        )

    @raises(AttributeError)
    def test_address_must_have_postal_code(self):
        ShipStationAddress(
            street1='123 main st',
            city='some city',
            state='some state',
            postal_code=''
        )

    @raises(AttributeError)
    def test_address_residential_is_bool_or_empty(self):
        ShipStationAddress(
            street1='123 main st',
            city='some city',
            state='some state',
            postal_code='12345',
            residential='something'
        )
