from shipstation.data.base import ShipStationBase
from shipstation.data.customs_item import ShipStationCustomsItem


class ShipStationInternationalOptions(ShipStationBase):
    CONTENTS_VALUES = (
        'merchandise',
        'documents',
        'gift',
        'returned_goods',
        'sample'
    )

    NON_DELIVERY_OPTIONS = (
        'return_to_sender',
        'treat_as_abandoned'
    )

    def __init__(self, contents=None, non_delivery=None):
        self.customs_items = []
        self.set_contents(contents)
        self.set_non_delivery(non_delivery)

    def set_contents(self, contents):
        if contents:
            if contents not in self.CONTENTS_VALUES:
                raise AttributeError('contents value not valid')
            self.contents = contents
        else:
            self.contents = None

    def add_customs_item(self, customs_item):
        if customs_item:
            if not isinstance(customs_item, ShipStationCustomsItem):
                raise AttributeError('must be of type ShipStationCustomsItem')
            self.customs_items.append(customs_item)

    def get_items(self):
        return self.customs_items

    def get_items_as_dicts(self):
        return [x.as_dict() for x in self.customs_items]

    def set_non_delivery(self, non_delivery):
        if non_delivery:
            if non_delivery not in self.NON_DELIVERY_OPTIONS:
                raise AttributeError('non_delivery value is not valid')
            self.non_delivery = non_delivery
        else:
            self.non_delivery = None

    def as_dict(self):
        d = super(ShipStationInternationalOptions, self).as_dict()

        d['customsItems'] = self.get_items_as_dicts()

        return d
