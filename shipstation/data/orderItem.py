from shipstation.data.base import ShipStationBase
from shipstation.data.weight import ShipStationWeight


class ShipStationItem(ShipStationBase):
    def __init__(self, key=None, sku=None, name=None, image_url=None,
                 quantity=None, unit_price=None, warehouse_location=None,
                 options=None):
        self.key = key
        self.sku = sku
        self.name = name
        self.image_url = image_url
        self.weight = None
        self.quantity = quantity
        self.unit_price = unit_price
        self.warehouse_location = warehouse_location
        self.options = options

    def set_weight(self, weight):
        if type(weight) is not ShipStationWeight:
            raise AttributeError('Should be type ShipStationWeight')

        self.weight = weight

    def as_dict(self):
        d = super(ShipStationItem, self).as_dict()

        if self.weight:
            d['weight.py'] = self.weight.as_dict()

        return d
