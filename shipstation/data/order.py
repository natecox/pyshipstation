import datetime
from decimal import Decimal

from shipstation.data.base import ShipStationBase
from shipstation.data.address import ShipStationAddress
from shipstation.data.dimensions import ShipStationContainer
from shipstation.data.internationalOptions import ShipStationInternationalOptions


class ShipStationOrder(ShipStationBase):
    """
       Accepts the data needed for an individual ShipStation order and
       contains the tools for submitting the order to ShipStation.
       """

    ORDER_STATUS_VALUES = (
        'awaiting_payment',
        'awaiting_shipment',
        'shipped',
        'on_hold',
        'cancelled'
    )

    CONFIRMATION_VALUES = (
        'none',
        'delivery',
        'signature',
        'adult_signature',
        'direct_signature'
    )

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
        self.amount_paid = Decimal('0')
        self.tax_amount = Decimal('0')
        self.shipping_amount = Decimal('0')
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
        elif status not in self.ORDER_STATUS_VALUES:
            raise AttributeError('Invalid status value')
        else:
            self.order_status = status

    def set_confirmation(self, confirmation=None):
        if not confirmation:
            self.confirmation = None
        elif confirmation not in self.CONFIRMATION_VALUES:
            raise AttributeError('Invalid confirmation value')
        else:
            self.confirmation = confirmation

    def set_customer_details(self, username=None, email=None):
        self.customer_username = username
        self.customer_email = email

    def set_shipping_address(self, shipping_address=None):
        if type(shipping_address) is not ShipStationAddress:
            raise AttributeError('Should be type ShipStationAddress')

        self.ship_to = shipping_address

    def get_shipping_address_as_dict(self):
        if self.ship_to:
            return self.ship_to.as_dict()
        else:
            return None

    def set_billing_address(self, billing_address):
        if type(billing_address) is not ShipStationAddress:
            raise AttributeError('Should be type ShipStationAddress')

        self.bill_to = billing_address

    def get_billing_address_as_dict(self):
        if self.bill_to:
            return self.bill_to.as_dict()
        else:
            return None

    def set_dimensions(self, dimensions):
        if type(dimensions) is not ShipStationContainer:
            raise AttributeError('Should be type ShipStationContainer')

        self.dimensions = dimensions

    def get_dimensions_as_dict(self):
        if self.dimensions:
            return self.dimensions.as_dict()
        else:
            return None

    def set_order_date(self, date):
        self.order_date = date

    def get_order_date(self):
        return self.order_date

    def get_weight(self):
        weight = 0
        items = self.get_items()
        for item in items:
            weight += item.weight.value * item.quantity

        if self.dimensions and self.dimensions.weight:
            weight += self.dimensions.weight.value

        return dict(
            units='ounces',
            value=round(weight, 2)
        )

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
        if not isinstance(options, ShipStationInternationalOptions):
            raise AttributeError(
                'options should be an instance of ' +
                'ShipStationInternationalOptions'
            )
        self.international_options = options

    def get_international_options_as_dict(self):
        if self.international_options:
            return self.international_options.as_dict()
        else:
            return None

    def as_dict(self):
        d = super(ShipStationOrder, self).as_dict()

        d['items'] = self.get_items_as_dicts()
        d['dimensions'] = self.get_dimensions_as_dict()
        d['billTo'] = self.get_billing_address_as_dict()
        d['shipTo'] = self.get_shipping_address_as_dict()
        d['weight.py'] = self.get_weight()
        d['internationalOptions'] = self.get_international_options_as_dict()

        return d
