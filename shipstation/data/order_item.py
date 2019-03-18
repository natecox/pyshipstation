from shipstation.data.base import ShipStationBase
from shipstation.data.weight import ShipStationWeight


class ShipStationItem(ShipStationBase):
    def __init__(
            self,
            line_item_key=None,
            sku=None,
            name='',
            image_url=None,
            quantity=None,
            unit_price=None,
            warehouse_location=None,
            options=None,
            tax_amount=None,
            shipping_amount=None,
            fulfillment_sku=None,
            adjustment=None,
            upc=None,
            product_id=None
    ):
        self.line_item_key = line_item_key
        self.sku = sku
        self.name = name
        self.image_url = image_url
        self.weight = None
        self.quantity = quantity
        self.unit_price = unit_price
        self.tax_amount = tax_amount
        self.shipping_amount = shipping_amount
        self.warehouse_location = warehouse_location
        self.options = options
        self.product_id = product_id
        self.fulfillment_sku = fulfillment_sku
        self.adjustment = adjustment
        self.upc = upc

        if product_id and not isinstance(product_id, int):
            raise AttributeError('Product id must be int or empty')
        if adjustment and not isinstance(adjustment, bool):
            raise AttributeError('Residential must be bool or empty')

    def set_weight(self, weight):
        if type(weight) is not ShipStationWeight:
            raise AttributeError('Should be type ShipStationWeight')

        self.weight = weight

    def as_dict(self):
        d = super(ShipStationItem, self).as_dict()

        if self.weight:
            d['weight.py'] = self.weight.as_dict()

        return d
