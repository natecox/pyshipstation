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
        self.phone = phone
        self.residential = residential

        if country:
            self.country = country.upper()
        else:
            self.country = None

        if not name:
            raise AttributeError('Name must not be empty')
        if residential and not isinstance(residential, bool):
            raise AttributeError('Residential must be bool or empty')
        if country and len(country) is not 2:
            raise AttributeError('Country must be two characters')
