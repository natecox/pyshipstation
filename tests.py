import unittest


class ShipStationTests(unittest.TestCase):

    def test_shipstation_imports_correctly(self):
        from shipstation.api import ShipStation
        ShipStation('123', '456')
