from shipstation.data.base import ShipStationBase


class ShipStationAddress(ShipStationBase):
    def __init__(self, name=None, company=None, street1=None, street2=None,
                 street3=None, city=None, state=None, postal_code=None,
                 country=None, phone=None, residential=None):
        self.name = name
        self.company = company
        self.street1 = street1
        self.street2 = street2
        self.street3 = street3
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.phone = phone
        self.residential = residential
