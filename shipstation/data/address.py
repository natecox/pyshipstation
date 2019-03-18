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
        self.country = country.upper()
        self.phone = phone
        self.residential = residential

        if not street1:
            raise AttributeError('Street1 may not be empty')
        if not city:
            raise AttributeError('City may not be empty')
        if not state:
            raise AttributeError('State may not be empty')
        if not postal_code:
            raise AttributeError('Postal code may not be empty')
        if residential and not isinstance(residential, bool):
            raise AttributeError('Residential must be bool or empty')
        if len(country) is not 2:
            raise AttributeError('Country must be two characters')
