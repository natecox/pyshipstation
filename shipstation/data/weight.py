from shipstation.data.base import ShipStationBase
from decimal import Decimal


class ShipStationWeight(ShipStationBase):
    def __init__(self, value, units):
        self.units = units
        self.value = value

        if not value or not isinstance(value, (int, float, Decimal)):
            raise AttributeError('Value must not be empty and must be a number')
        if not units or units not in ['pounds', 'ounces', 'grams']:
            raise AttributeError('Units must not be empty and be `pounds`, `ounces` or `grams`')
