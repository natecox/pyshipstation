from unittest import TestCase
from shipstation.api import ShipStationWeight


class ShipStationWeightTests(TestCase):

    def setUp(self):
        self.units = 2
        self.value = 4
        self.weight = ShipStationWeight(units=self.units,
                                        value=self.value)

    def test_weight_init(self):
        self.assertEqual(self.weight.units, self.units)
        self.assertEqual(self.weight.value, self.value)
