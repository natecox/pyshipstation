import unittest
from nose.tools import raises
from shipstation.api import *


class ShipStationOrderItemTest(unittest.TestCase):
    def test_order_item_init_works(self):
        self.json = {
            'line_item_key': 'some key',
            'sku': 'some sku',
            'name': 'some name',
            'image_url': 'some url',
            'quantity': 1,
            'unit_price': 10,
            'tax_amount': 0.15,
            'shipping_amount': None,
            'warehouse_location': 'some location',
            'options': None,
            'product_id': 12345,
            'fulfillment_sku': 'some fulfillment sku',
            'adjustment': None,
            'upc': 'some upc'
        }

        self.json_with_weight = self.json.copy()

        self.json_with_weight['weight'] = None

        self.ss_order_item = ShipStationItem(**self.json)

        self.assertDictEqual(
            self.ss_order_item.__dict__,
            self.json_with_weight
        )

    @raises(AttributeError)
    def test_order_item_must_have_number_product_id(self):
        ShipStationItem(
            product_id='not a number'
        )

    @raises(AttributeError)
    def test_order_item_must_have_bool_adjustment(self):
        ShipStationItem(
            adjustment='not a bool'
        )

    @raises(AttributeError)
    def test_order_item_must_must_be_weight(self):
        ShipStationItem().set_weight(weight='not a weight')

    def test_order_item_must_set_weight_correctly(self):
        self.order_item = ShipStationItem()
        self.order_item.set_weight(weight=ShipStationWeight(value=1))

        print(self.order_item)

        self.assertEqual(self.order_item.weight.value, 1)
