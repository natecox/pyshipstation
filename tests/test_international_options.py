from decimal import Decimal
from unittest import TestCase
from nose.tools import raises

from shipstation.api import (ShipStation, ShipStationOrder,
                             ShipStationInternationalOptions,
                             ShipStationCustomsItem)


class ShipStationIntlOptionsTests(TestCase):

    def setUp(self):
        self.ss = ShipStation('123', '456')
        self.ss_order = ShipStationOrder()
        self.ss_intl = ShipStationInternationalOptions()

        self.ss_customs_item = ShipStationCustomsItem(
            description='customs item',
            quantity=1,
            value=Decimal('10.00'),
            harmonized_tariff_code='code',
            country_of_origin='US'
        )

    def test_order_accepts_international_options(self):
        self.ss_intl.add_customs_item(self.ss_customs_item)
        self.ss_intl.set_contents('documents')
        self.ss_intl.set_non_delivery('return_to_sender')

        self.ss_order.set_international_options(self.ss_intl)

        expected = self.ss_intl.as_dict()
        actual = self.ss_order.as_dict()['internationalOptions']

        self.assertDictEqual(expected, actual)

    @raises(AttributeError)
    def test_international_options_contents_must_be_valid(self):
        self.ss_intl.set_contents('something_else')

    @raises(AttributeError)
    def test_international_options_non_delivery_must_be_valid(self):
        self.ss_intl.set_non_delivery('something_else')

    @raises(AttributeError)
    def test_international_options_item_must_be_valid(self):
        self.ss_intl.add_customs_item('something_else')

    def test_international_options_get_items(self):
        self.ss_intl.add_customs_item(self.ss_customs_item)
        self.assertEqual(self.ss_intl.get_items(), [self.ss_customs_item])
