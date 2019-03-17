from shipstation.data.base import ShipStationBase
from shipstation.data.weight import ShipStationWeight

from decimal import Decimal


class ShipStationContainer(ShipStationBase):
    def __init__(self, units, length, width, height):
        self.units = units
        self.length = length
        self.width = width
        self.height = height
        self.weight = None

        if not units:
            raise AttributeError('Units must not be empty')
        if units not in ['inches', 'centimeters']:
            raise AttributeError('Units must be `inches` or `centimeters`')
        if not isinstance(length, (Decimal, int, float)):
            raise AttributeError('Length must be a number')
        if not isinstance(width, (Decimal, int, float)):
            raise AttributeError('Length must be a number')
        if not isinstance(height, (Decimal, int, float)):
            raise AttributeError('Length must be a number')

    def set_weight(self, weight):
        if type(weight) is not ShipStationWeight:
            raise AttributeError('Should be type ShipStationWeight')

        self.weight = weight

    def as_dict(self):
        d = super(ShipStationContainer, self).as_dict()

        if self.weight:
            d['weight.py'] = self.weight.as_dict()

        return d
