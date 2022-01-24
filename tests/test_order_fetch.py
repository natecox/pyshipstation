import unittest
import pytest
from shipstation.api import *


class ShipStationApiTests(unittest.TestCase):
    def setUp(self):
        self.ss = ShipStation("123", "456")

    def tearDown(self):
        self.ss = None

    @pytest.mark.xfail(raises=AttributeError)
    def test_fetch_orders_must_be_dict(self):
        self.ss.fetch_orders(parameters="non dict")

    @pytest.mark.xfail(raises=AttributeError)
    def test_fetch_orders_must_use_correct_parameter(self):
        self.ss.fetch_orders(parameters={"bad": "not good"})
