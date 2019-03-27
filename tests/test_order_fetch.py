import unittest
from nose.tools import raises
from shipstation.api import *


class ShipStationApiTests(unittest.TestCase):
    def setUp(self):
        self.ss = ShipStation('123', '456')

    def tearDown(self):
        self.ss = None

    @raises(AttributeError)
    def test_fetch_orders_must_be_dict(self):
        self.ss.fetch_orders(parameters="non dict")

    @raises(AttributeError)
    def test_fetch_orders_must_use_correct_parameter(self):
        self.ss.fetch_orders(parameters={'bad': 'not good'})
