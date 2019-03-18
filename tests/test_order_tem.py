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
            'warehouse_location': 'some location',
            'options': None,
        }

        self.json_with_weight = self.json.copy()

        self.json_with_weight['weight'] = None

        self.ss_order_item = ShipStationItem(**self.json)

        self.assertDictEqual(
            self.ss_order_item.__dict__,
            self.json_with_weight
        )

    @raises(AttributeError)
    def test_order_item_must_must_be_weight(self):
        ShipStationItem().set_weight(weight='not a weight')

    def test_order_item_must_set_weight_correctly(self):
        self.order_item = ShipStationItem()
        self.order_item.set_weight(weight=ShipStationWeight(value=1, units='grams'))

        print(self.order_item)

        self.assertEqual(self.order_item.weight.value, 1)
