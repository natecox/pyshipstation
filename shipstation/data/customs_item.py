from shipstation.data.base import ShipStationBase
from decimal import Decimal


class ShipStationCustomsItem(ShipStationBase):
    def __init__(self,
                 description=None,
                 quantity=1,
                 value=Decimal('0'),
                 harmonized_tariff_code=None,
                 country_of_origin=None):
        self.description = description
        self.quantity = quantity
        self.value = value
        self.harmonized_tariff_code = harmonized_tariff_code

        if country_of_origin:
            self.country_of_origin = country_of_origin.upper()
        else:
            self.country_of_origin = None

        if not self.description:
            raise AttributeError('description may not be empty')
        if not self.harmonized_tariff_code:
            raise AttributeError('harmonized_tariff_code may not be empty')
        if not self.country_of_origin:
            raise AttributeError('country_of_origin may not be empty')
        if len(self.country_of_origin) is not 2:
            raise AttributeError('country_of_origin must be two characters')
        if not isinstance(value, Decimal):
            raise AttributeError('value must be decimal')
