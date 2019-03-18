import unittest
from nose.tools import raises
from shipstation.api import *


class ShipStationWeightTest(unittest.TestCase):
    def test_weight_init_works(self):
        self.json = {
            'units': 'grams',
            'value': 3
        }

        self.ss_dimensions = ShipStationWeight(**self.json)

        self.assertDictEqual(
            self.ss_dimensions.__dict__,
            self.json
        )

    @raises(AttributeError)
    def test_weight_value_must_be_set(self):
        ShipStationWeight(
            value='',
            units='grams'
        )

    @raises(AttributeError)
    def test_weight_value_must_be_number(self):
        ShipStationWeight(
            value='not a number',
            units='grams'
        )

    @raises(AttributeError)
    def test_weight_units_must_be_set(self):
        ShipStationWeight(
            value=1,
            units=''
        )

    @raises(AttributeError)
    def test_weight_units_must_be_correct_term(self):
        ShipStationWeight(
            value=1,
            units='monkeys'
        )
