import unittest
from nose.tools import raises
from shipstation.api import *
from shipstation.utils import require_type


class UtilityTests(unittest.TestCase):
    def test_none_passes(self):
        require_type(None, dict)

    def test_order_type(self):
        sso = ShipStationOrder()
        require_type(sso, ShipStationOrder)

    @raises(AttributeError)
    def test_address(self):
        address = {"name": "test name", "company": "test_company"}
        require_type(address, ShipStationAddress)

    def test_custom_message(self):
        msg = "I'm a custom error message"
        try:
            sso = ShipStationOrder()  # ShipStationOrder != ShipStationItem
            require_type(sso, ShipStationItem, msg)
        except Exception as e:
            self.assertEqual(e.args[0], msg)
