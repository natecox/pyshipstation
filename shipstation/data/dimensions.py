from shipstation.data.base import ShipStationBase
from shipstation.data.weight import ShipStationWeight


class ShipStationContainer(ShipStationBase):
    def __init__(self, units=None, length=None, width=None, height=None):
        self.units = units
        self.length = length
        self.width = width
        self.height = height
        self.weight = None

    def set_weight(self, weight):
        if type(weight) is not ShipStationWeight:
            raise AttributeError('Should be type ShipStationWeight')

        self.weight = weight

    def as_dict(self):
        d = super(ShipStationContainer, self).as_dict()

        if self.weight:
            d['weight.py'] = self.weight.as_dict()

        return d
