# Shipstation API Python Bindings
This package provides the basic API bindings for interacting with
[ShipStation](http://www.shipstation.com/) via Python.

## Connecting to ShipStation
pyshipstation provides the class `ShipStation` to instantiate a new connection
to ShipStation.

    from shipstation.api import *

    api_key = '[your key]'
    api_secret = '[your secret]'

    ss = ShipStation(key=api_key, secret=api_secret)
    
## ShipStationOrder
Orders can be provided using the `ShipStationOrder` class.

The constructor accepts both `order_key` and `order_number`, but in practice
only `order_number` is actually required. ShipStation will generate a unique
key for you on submission.

    id = '[a reference number]'
    ss_order = ShipStationOrder(order_number=id)
    
### Setting The Order Status
Order status is set using the `set_status` method.

    ss_order.set_status('awaiting_shipment')
    
### Setting Customer Details
Customer username and email can be set with the `set_customer_deails` method.

    ss_order.set_customer_details(
        username='foobar',
        email='foo@bar.org'
    )
    
### Setting The Shipping and Billing Addresses
Addresses are represented as a `ShipStationAddress` instance, and set
using the `set_shipping_address` or `set_billing_address` method.

    shipping_address = ShipStationAddress(...)
    billing_address = ShipStationAddress(...)
    
    ss_order.set_shipping_address(shipping_address)
    ss_order.set_billing_address(billing_address)
    
### Setting The Package Dimensions and Weight
Package dimensions are represented as a `ShipStationContainer` instance, and
set using the `set_dimensions` method.

    container = ShipStationContainer(...)
    ss_order.set_dimensions(container)
    
### Adding Line Items
Line items are represented as a `ShipStationItem` instance, and are added
individually using the `add_item` method.

    item = ShipStationItem(...)
    ss_order.add_item(item)
    
## ShipStationWeight
This corresponds to the Weight model in ShipStation, and accepts
`units` and `value`.

    weight = ShipStationWeight(units='ounces', value=12)
    
## ShipStationContainer
This corresponds to the Dimensions model in ShipStation. 

Weight is represented as a `ShipStationWeight` instance and added via the 
`set_weight` method.

    weight = ShipStationWeight(...)
    ss_container = ShipStationContainer(
        units='inches',
        length=5,
        width=5,
        height=5
    )
    ss_container.set_weight(weight)
    
## ShipStationItem
This corresponds to the Product model in ShipStation. 

Weight is represented as a `ShipStationWeight` instance and added via the 
`set_weight` method.

    weight = ShipStationWeight(...)
    ss_item = ShipStationItem(
        sku='[your sku]',
        name='[item name]',
        image_url='[item image url]',
        quantity=1,
        unit_price=10
    )
    ss_item.set_weight(weight)

## ShipStationAddress
This corresponds to the Address model in ShipStation

    ss_shipping_address = ShipStationAddress(
        name='[customer name]',
        street1='[street line 1]',
        street2='[street line 2]',
        street3='[street line 3]',
        city='[city]',
        state='[state]',
        postal_code=['zip code'],
        country='[two letter country code]'
    )
