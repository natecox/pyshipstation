import json
import requests


class ShipStationBase(object):
    @classmethod
    def to_camel_case(cls, name):
        tokens = name.lower().split('_')
        first_word = tokens.pop(0)
        return first_word + ''.join(x.title() for x in tokens)

    def as_dict(self):
        d = dict()

        for key, value in self.__dict__.iteritems():
            key = self.to_camel_case(key)
            if value is None:
                d[key] = None
            else:
                d[key] = str(value)

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
        self.order_date = None
        self.order_status = None
        self.bill_to = None
        self.ship_to = None

        # Optional attributes
        self.order_key = order_key
        self.payment_date = None
        self.customer_username = None
        self.customer_email = None
        self.items = []
        self.amount_paid = None
        self.tax_amount = None
        self.shipping_amount = None
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

    def as_dict(self):
        d = super(ShipStationOrder, self).as_dict()

        d['items'] = self.get_items_as_dicts()
        d['dimensions'] = self.get_dimensions_as_dict()
        d['billTo'] = self.get_billing_address_as_dict()
        d['shipTo'] = self.get_shipping_address_as_dict()
        d['weight'] = self.get_weight()

        return d


class ShipStation:
    """
    Handles the details of connecting to and querying a ShipStation account.
    """

    def __init__(self, key=None, secret=None):
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
        print r.json()

    def post(self, endpoint='', data=None):
        url = '{}{}'.format(self.url, endpoint)
        headers = {'content-type': 'application/json'}
        requests.post(
            url,
            auth=(self.key, self.secret),
            data=data,
            headers=headers
        )
