import unittest
from nose.tools import raises
from shipstation.api import *


class ShipStationDimensionsTest(unittest.TestCase):
    def test_dimensions_init_works(self):
        self.json = {
            'units': 'inches',
            'length': 1,
            'width': 2,
            'height': 3
        }

        self.json_with_weight = self.json.copy()

        self.json_with_weight['weight'] = None

        self.ss_dimensions = ShipStationContainer(**self.json)

        self.assertDictEqual(
            self.ss_dimensions.__dict__,
            self.json_with_weight
        )

    @raises(AttributeError)
    def test_dimensions_must_have_length(self):
        ShipStationContainer(
            units='inches',
            width=1,
            height=2,
            length=''
        )

    @raises(AttributeError)
    def test_dimensions_must_have_height(self):
        ShipStationContainer(
            units='inches',
            width=1,
            height='',
            length=3
        )

    @raises(AttributeError)
    def test_dimensions_must_have_width(self):
        ShipStationContainer(
            units='inches',
            width='',
            height=2,
            length=3
        )

    @raises(AttributeError)
    def test_dimensions_units_must_be_correct(self):
        ShipStationContainer(
            units='cm',
            width=1,
            height=2,
            length=3
        )
