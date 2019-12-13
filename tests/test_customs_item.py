import unittest
import pytest
from shipstation.api import *
from decimal import Decimal


class ShipStationTests(unittest.TestCase):
    def setUp(self):
        self.ss = ShipStation("123", "456")
        self.ss_order = ShipStationOrder()
        self.ss_intl = ShipStationInternationalOptions()

        self.ss_customs_item1 = ShipStationCustomsItem(
            description="customs item",
            quantity=1,
            value=Decimal("10.00"),
            harmonized_tariff_code="code",
            country_of_origin="US",
        )
        self.ss_customs_item2 = ShipStationCustomsItem(
            description="customs item two",
            quantity=2,
            value=Decimal("20.00"),
            harmonized_tariff_code="code",
            country_of_origin="US",
        )

    def tearDown(self):
        self.ss = None
        self.ss_order = None
        self.ss_intl = None
        self.ss_customs_item = None

    def test_intl_options_accepts_customs_item(self):
        self.ss_intl.add_customs_item(self.ss_customs_item1)
        self.ss_intl.add_customs_item(self.ss_customs_item2)

        expected = 2
        actual = len(self.ss_intl.as_dict()["customsItems"])

        self.assertEqual(expected, actual)

    @pytest.mark.xfail(raises=AttributeError)
    def test_customs_item_must_have_description(self):
        ShipStationCustomsItem(
            description="", harmonized_tariff_code="test", country_of_origin="us"
        )

    @pytest.mark.xfail(raises=AttributeError)
    def test_customs_item_must_have_tariff_code(self):
        ShipStationCustomsItem(
            description="test", harmonized_tariff_code="", country_of_origin="us"
        )

    @pytest.mark.xfail(raises=AttributeError)
    def test_customs_item_must_have_country_code(self):
        ShipStationCustomsItem(description="test", harmonized_tariff_code="test")

    @pytest.mark.xfail(raises=AttributeError)
    def test_customs_item_must_have_two_character_country_code(self):
        ShipStationCustomsItem(
            description="test",
            harmonized_tariff_code="test",
            country_of_origin="something_else",
        )
