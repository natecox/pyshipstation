from shipstation.data.base import ShipStationBase


class ShipStationWeight(ShipStationBase):
    def __init__(self, units=None, value=None):
        self.units = units
        self.value = value
