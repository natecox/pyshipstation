import json
import requests
import pprint
import datetime
from decimal import Decimal


class ShipStationBase(object):
    @classmethod
    def to_camel_case(cls, name):
        tokens = name.lower().split('_')
        first_word = tokens.pop(0)
        return first_word + ''.join(x.title() for x in tokens)

    def as_dict(self):
        d = dict()

        for key, value in self.__dict__.items():
            key = self.to_camel_case(key)
            if value is None:
                d[key] = None
            else:
                d[key] = str(value)

        return d


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
        self.country_of_origin = country_of_origin

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
        if type(weight) is not ShipStationWeight:
            raise AttributeError('Should be type ShipStationWeight')

        self.weight = weight

    def as_dict(self):
        d = super(ShipStationContainer, self).as_dict()

        if self.weight:
            d['weight'] = self.weight.as_dict()

        return d


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
            d['weight'] = self.weight.as_dict()

        return d


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

    # TODO: add method for adding confirmation which respects these values.
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
        d['weight'] = self.get_weight()
        d['internationalOptions'] = self.get_international_options_as_dict()

        return d


class ShipStation:
    """
    Handles the details of connecting to and querying a ShipStation account.
    """

    def __init__(self, key=None, secret=None, debug=False):
        """
        Connecting to ShipStation required an account and a
        :return:
        """

        if key is None:
            raise AttributeError('Key must be supplied.')
        if secret is None:
            raise AttributeError('Secret must be supplied.')

        self.url = 'https://ssapi.shipstation.com'

        self.key = key
        self.secret = secret
        self.orders = []

        self.debug = debug

    def add_order(self, order):
        if type(order) is not ShipStationOrder:
            raise AttributeError('Should be type ShipStationOrder')
        self.orders.append(order)

    def get_orders(self):
        return self.orders

    def submit_orders(self):
        for order in self.orders:
            self.post(
                endpoint='/orders/createorder',
                data=json.dumps(order.as_dict())
            )

    def get(self, endpoint=''):
        url = '{}{}'.format(self.url, endpoint)
        r = requests.get(url, auth=(self.key, self.secret))
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())

    def post(self, endpoint='', data=None):
        url = '{}{}'.format(self.url, endpoint)
        headers = {'content-type': 'application/json'}
        r = requests.post(
            url,
            auth=(self.key, self.secret),
            data=data,
            headers=headers
        )
        if self.debug:
            pprint.PrettyPrinter(indent=4).pprint(r.json())
