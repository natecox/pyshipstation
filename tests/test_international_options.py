from decimal import Decimal
import pytest
from shipstation.models import *
from shipstation.api import ShipStation
import unittest

class ShipStationTests(unittest.TestCase):
    def setUp(self):
        self.ss = ShipStation("123", "456")
        self.ss_order = ShipStationOrder()
        self.ss_intl = ShipStationInternationalOptions()

        self.ss_customs_item = ShipStationCustomsItem(
            description="customs item",
            quantity=1,
            value=Decimal("10.00"),
            harmonized_tariff_code="code",
            country_of_origin="US",
        )

    def tearDown(self):
        self.ss = None
        self.ss_order = None
        self.ss_intl = None
        self.ss_customs_item = None

    def test_order_accepts_international_options(self):
        self.ss_intl.add_customs_item(self.ss_customs_item)
        self.ss_intl.set_contents("documents")
        self.ss_intl.set_non_delivery("return_to_sender")

        self.ss_order.set_international_options(self.ss_intl)

        expected = self.ss_intl.as_dict()
        actual = self.ss_order.as_dict()["internationalOptions"]

        self.assertDictEqual(expected, actual)

    @pytest.mark.xfail(raises=AttributeError)
    def test_international_options_contents_must_be_valid(self):
        self.ss_intl.set_contents("something_else")

    @pytest.mark.xfail(raises=AttributeError)
    def test_international_options_non_delivery_must_be_valid(self):
        self.ss_intl.set_non_delivery("something_else")
