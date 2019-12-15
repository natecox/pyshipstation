from shipstation.constants import *
from decimal import Decimal
import datetime

__all__ = [
    'ShipStationAddress',
    'ShipStationAdvancedOptions',
    'ShipStationBase',
    'ShipStationContainer',
    'ShipStationCustomsItem',
    'ShipStationInsuranceOptions',
    'ShipStationInternationalOptions',
    'ShipStationItem',
    'ShipStationOrder',
    'ShipStationStatusMapping',
    'ShipStationStore',
    'ShipStationWeight'
]


class ShipStationBase(object):
    @classmethod
    def to_camel_case(cls, name):
        tokens = name.lower().split("_")
        first_word = tokens.pop(0)
        return first_word + "".join(x.title() for x in tokens)

    def as_dict(self):
        d = dict()
        for key, value in self.__dict__.items():
            key = self.to_camel_case(key)
            if value is None:
                d[key] = None
            else:
                d[key] = str(value)
        return d

    def require_attribute(self, attribute):
        if not getattr(self, attribute):
            raise AttributeError("'{}' is a required attribute".format(attribute))

    def require_type(self, item, required_type, message=""):
        if item is None:
            return
        if not isinstance(item, required_type):
            if message:
                raise AttributeError(message)
            raise AttributeError("must be of type {}".format(required_type))

    def require_membership(self, value, other):
        if value not in other:
            raise AttributeError("'{}' is not a valid option for".format(value))

    def _validate_parameters(self, parameters, valid_parameters):
        self.require_type(parameters, dict)
        self.require_membership(parameters, valid_parameters)
        return {self.to_camel_case(key): value for key, value in parameters.items()}


class ShipStationCustomsItem(ShipStationBase):
    def __init__(
        self,
        description=None,
        quantity=1,
        value=Decimal("0"),
        harmonized_tariff_code=None,
        country_of_origin=None,
    ):
        self.description = description
        self.quantity = quantity
        self.value = value
        self.harmonized_tariff_code = harmonized_tariff_code
        self.country_of_origin = country_of_origin

        self.require_attribute('description')
        self.require_attribute('harmonized_tariff_code')
        self.require_attribute('country_of_origin')
        self.require_attribute('description')
        self.require_type(value, Decimal)
        if len(self.country_of_origin) is not 2:
            raise AttributeError("country_of_origin must be two characters")


class ShipStationInternationalOptions(ShipStationBase):
    def __init__(self, contents=None, non_delivery="return_to_sender"):
        self.customs_items = []
        self.set_contents(contents)
        self.set_non_delivery(non_delivery)

    def set_contents(self, contents):
        if contents:
            if contents not in CONTENTS_VALUES:
                raise AttributeError("contents value not valid")
            self.contents = contents
        else:
            self.contents = None

    def add_customs_item(self, customs_item):
        self.require_type(customs_item, ShipStationCustomsItem)
        self.customs_items.append(customs_item)

    def get_items(self):
        return self.customs_items

    def get_items_as_dicts(self):
        return [x.as_dict() for x in self.customs_items]

    def set_non_delivery(self, non_delivery):
        if non_delivery:
            if non_delivery not in NON_DELIVERY_OPTIONS:
                raise AttributeError("non_delivery value is not valid")
            self.non_delivery = non_delivery
        else:
            self.non_delivery = None

    def as_dict(self):
        d = super(ShipStationInternationalOptions, self).as_dict()
        d["customsItems"] = self.get_items_as_dicts()
        return d


class ShipStationWeight(ShipStationBase):
    def __init__(self, units=None, value=None):
        self.units = units
        self.value = value


class ShipStationContainer(ShipStationBase):
    def __init__(self, units=None, length=None, width=None, height=None):
        self.units = units
        self.length = length
        self.width = width
        self.height = height
        self.weight = None

    def set_weight(self, weight):
        self.require_type(weight, ShipStationWeight)
        self.weight = weight

    def set_units(self, units):
        self.require_membership(units)
        self.units = units

    def as_dict(self):
        d = super(ShipStationContainer, self).as_dict()
        return __setattr__(d, 'weight', self.weight.as_dict()) if self.weight else d
        #
        # if self.weight:
        #     d["weight"] = self.weight.as_dict()
        #
        # return d


class ShipStationItem(ShipStationBase):
    def __init__(
        self,
        key=None,
        sku=None,
        name=None,
        image_url=None,
        quantity=None,
        unit_price=None,
        warehouse_location=None,
        options=None,
    ):
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
        self.require_type(weight, ShipStationWeight)
        self.weight = weight

    def as_dict(self):
        d = super(ShipStationItem, self).as_dict()
        return __setattr__(d, 'weight', self.weight.as_dict()) if self.weight else d
        # if self.weight:
        #     d["weight"] = self.weight.as_dict()
        #
        # return d


class ShipStationAddress(ShipStationBase):
    def __init__(
        self,
        name=None,
        company=None,
        street1=None,
        street2=None,
        street3=None,
        city=None,
        state=None,
        postal_code=None,
        country=None,
        phone=None,
        residential=None,
    ):
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


class ShipStationOrder(ShipStationBase):
    """
    Accepts the data needed for an individual ShipStation order and
    contains the tools for submitting the order to ShipStation.
    """
    def __init__(self, order_key=None, order_number=None):

        # Required attributes
        self.order_number = order_number
        self.order_date = datetime.datetime.now().isoformat()
        self.order_status = None
        self.bill_to = None
        self.ship_to = None

        # Optional attributes
        self.order_key = order_key
        self.payment_date = None
        self.customer_username = None
        self.customer_email = None
        self.items = []
        self.amount_paid = Decimal("0")
        self.tax_amount = Decimal("0")
        self.shipping_amount = Decimal("0")
        self.customer_notes = None
        self.internal_notes = None
        self.gift = None
        self.payment_method = None
        self.carrier_code = None
        self.service_code = None
        self.package_code = None
        self.confirmation = None
        self.ship_date = None
        self.dimensions = None
        self.insurance_options = None
        self.international_options = None
        self.advanced_options = None

    def set_status(self, status=None):
        if not status:
            self.order_status = None
        elif status not in ORDER_STATUS_VALUES:
            raise AttributeError("Invalid status value")
        else:
            self.order_status = status

    def set_customer_details(self, username=None, email=None):
        self.customer_username = username
        self.customer_email = email

    def set_shipping_address(self, shipping_address=None):
        self.require_type(shipping_address, ShipStationAddress)
        self.ship_to = shipping_address

    def get_shipping_address_as_dict(self):
        return self.ship_to.as_dict() if self.ship_to else None

    def set_billing_address(self, billing_address):
        self.require_type(billing_address, ShipStationAddress)
        self.bill_to = billing_address

    def get_billing_address_as_dict(self):
        return self.bill_to.as_dict() if self.bill_to else None

    def set_dimensions(self, dimensions):
        self.require_type(dimensions, ShipStationContainer)
        self.dimensions = dimensions

    def get_dimensions_as_dict(self):
        return self.dimensions.as_dict() if self.dimensions else None

    def set_order_date(self, date):
        self.order_date = date

    def get_order_date(self):
        return self.order_date

    def get_weight(self):
        weight = 0
        items = self.get_items()
        weight = sum([item.weight.value * item.quantity for item in items])
        if self.dimensions and self.dimensions.weight:
            weight += self.dimensions.weight.value

        return dict(units="ounces", value=round(weight, 2))

    def add_item(self, item):
        """
        Adds a new item to the order with all of the required keys.
        """
        self.items.append(item)

    def get_items(self):
        return self.items

    def get_items_as_dicts(self):
        return [x.as_dict() for x in self.items]

    def set_international_options(self, options):
        self.require_type(options, ShipStationInternationalOptions)
        self.international_options = options

    def get_international_options_as_dict(self):
        return self.international_options.as_dict() if self.international_options else None

    def as_dict(self):
        d = super(ShipStationOrder, self).as_dict()

        d["items"] = self.get_items_as_dicts()
        d["dimensions"] = self.get_dimensions_as_dict()
        d["billTo"] = self.get_billing_address_as_dict()
        d["shipTo"] = self.get_shipping_address_as_dict()
        d["weight"] = self.get_weight()
        d["internationalOptions"] = self.get_international_options_as_dict()

        return d


class ShipStationAddress(ShipStationBase):
    def __init__(
        self,
        name=None,
        company=None,
        street1=None,
        street2=None,
        street3=None,
        city=None,
        state=None,
        postal_code=None,
        country=None,
        phone=None,
        residential=None,
    ):
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


class ShipStationAdvancedOptions(ShipStationBase):
    def __init__(
        self,
        warehouse_id=None,
        non_machineable=None,
        saturday_delivery=None,
        contains_alcohol=None,
        store_id=None,
        custom_field_1=None,
        custom_field_2=None,
        custom_field_3=None,
        soure=None,
        merged_or_split=None,
        merged_ids=None,
        bill_to_party=None,
        bill_to_account=None,
        bill_to_postal_code=None,
        bill_to_country_code=None,
        bill_to_my_other_account=None
    ):
        self.warehouse_id = warehouse_id
        self.non_machineable = non_machineable
        self.saturday_delivery = saturday_delivery
        self.contains_alcohol = contains_alcohol
        self.store_id = store_id
        self.custom_field_1 = custom_field_1
        self.custom_field_2 = custom_field_2
        self.custom_field_3 = custom_field_3
        self.source = source
        self.merged_or_split = merged_or_split
        self.merged_ids = merged_ids
        self.bill_to_party = bill_to_party
        self.bill_to_account = bill_to_account
        self.bill_to_postal_code = bill_to_postal_code
        self.bill_to_country_code = bill_to_country_code
        self.bill_to_my_other_account = bill_to_my_other_account


class ShipStationInsuranceOptions(ShipStationBase):
    def __init__(
        self,
        provider=None,
        insure_shipment=None,
        insured_value=None
    ):
        self.provider = provider
        self.insure_shipment = insure_shipment
        self.insured_value = insured_value


class ShipStationStatusMapping(ShipStationBase):
    def __init__(
        self,
        order_status=None,
        status_key=None
    ):
        self.order_status = order_status
        self.status_key = status_key

class ShipStationStore(ShipStationBase):
    def __init__(
        store_id=None,
        store_name=None,
        marketplace_id=None,
        marketplace_name=None,
        account_name=None,
        email=None,
        integration_url=None,
        active=None,
        company_name=None,
        phone=None,
        public_email=None,
        website=None,
        refresh_date=None,
        last_refresh_attempt=None,
        create_date=None,
        modify_date=None,
        auto_refresh=None,
        status_mappings=None
    ):
        self.store_id = store_id
        self.store_name = store_name
        self.marketplace_id = marketplace_id
        self.marketplace_name = marketplace_name
        self.account_name = account_name
        self.email = email
        self.integration_url = integration_url
        self.active = active
        self.company_name = company_name
        self.phone = phone
        self.public_email = public_email
        self.website = website
        self.refresh_date = refresh_date
        self.last_refresh_attempt = last_refresh_attempt
        self.create_date = create_date
        self.modify_date = modify_date
        self.auto_refresh = auto_refresh
        self.status_mappings = status_mappings
