__all__ = [
    "ORDER_STATUS_VALUES",
    "CONFIRMATION_VALUES",
    "ORDER_LIST_PARAMETERS",
    "CUSTOMER_LIST_PARAMETERS",
    "FULFILLMENT_LIST_PARAMETERS",
    "SHIPMENT_LIST_PARAMETERS",
    "CREATE_SHIPMENT_LABEL_OPTIONS",
    "GET_RATE_OPTIONS",
    "REQUIRED_RATE_OPTIONS",
    "CONTENTS_VALUES",
    "NON_DELIVERY_OPTIONS",
    "UPDATE_STORE_OPTIONS",
    "SUBSCRIBE_TO_WEBHOOK_OPTIONS",
    "SUBSCRIBE_TO_WEBHOOK_EVENT_OPTIONS",
    "WEIGHT_UNIT_OPTIONS",
]

# https://www.shipstation.com/developer-api/#/reference/orders/createupdate-order/create/update-order
# orderStatus
ORDER_STATUS_VALUES = (
    "awaiting_payment",
    "awaiting_shipment",
    "shipped",
    "on_hold",
    "cancelled",
)

# TODO: add method for adding confirmation which respects these values.
# https://www.shipstation.com/developer-api/#/reference/orders/createupdate-order/create/update-order
# confirmation
CONFIRMATION_VALUES = (
    "none",
    "delivery",
    "signature",
    "adult_signature",
    "direct_signature",
)


# https://www.shipstation.com/developer-api/#/reference/orders/list-orders/list-orders-with-parameters
ORDER_LIST_PARAMETERS = (
    "customer_name",
    "item_keyword",
    "create_date_start",
    "create_date_end",
    "modify_date_start",
    "modify_date_end",
    "order_date_start",
    "order_date_end",
    "order_number",
    "order_status",
    "payment_date_start",
    "payment_date_end",
    "store_id",
    "sort_by",
    "sort_dir",
    "page",
    "page_size",
)

# https://www.shipstation.com/developer-api/#/reference/carriers/list-services/list-customers
CUSTOMER_LIST_PARAMETERS = (
    "state_code",
    "country_code",
    "marketplace_id",
    "tag_id",
    "sort_by",
    "sort_dir",
    "page_size",
)

# https://www.shipstation.com/developer-api/#/reference/fulfillments/list-fulfillments/list-fulfillments-with-parameters
FULFILLMENT_LIST_PARAMETERS = (
    "fulfillment_id",
    "order_id",
    "order_number",
    "tracking_number",
    "recipient_name",
    "create_date_start",
    "create_date_end",
    "ship_date_start",
    "ship_date_end",
    "sort_by",
    "sort_dir",
    "page",
    "page_size",
)

# https://www.shipstation.com/developer-api/#/reference/shipments/list-shipments/list-shipments-with-parameters
SHIPMENT_LIST_PARAMETERS = (
    "recipient_name",
    "recipient_country_code",
    "order_number",
    "order_id",
    "carrier_code",
    "service_code",
    "tracking_number",
    "create_date_start",
    "create_date_end",
    "ship_date_start",
    "ship_date_end",
    "void_date_start",
    "void_date_end",
    "store_id",
    "include_shipment_items",
    "sort_by",
    "sort_dir",
    "page",
    "page_size",
)

# https://www.shipstation.com/developer-api/#/reference/shipments/create-shipment-label/create-shipment-label
CREATE_SHIPMENT_LABEL_OPTIONS = (
    "carrier_code",
    "service_code",
    "package_code",
    "confirmation",
    "ship_date",
    "weight",
    "dimensions",
    "ship_from",
    "ship_to",
    "insurance_options",
    "international_options",
    "advanced_options",
    "test_label",
)

# https://www.shipstation.com/developer-api/#/reference/shipments/get-rates/get-rates
GET_RATE_OPTIONS = (
    "carrier_code",
    "from_postal_code",
    "to_state",
    "to_country",
    "to_postal_code",
    "weight",
    "service_code",
    "package_code",
    "to_city",
    "dimensions",
    "confirmation",
    "residential",
)

REQUIRED_RATE_OPTIONS = (
    "carrier_code",
    "from_postal_code",
    "to_state",
    "to_country",
    "to_postal_code",
    "weight",
)

# https://www.shipstation.com/developer-api/#/reference/model-internationaloptions
CONTENTS_VALUES = ("merchandise", "documents", "gift", "returned_goods", "sample")

# https://www.shipstation.com/developer-api/#/reference/model-internationaloptions
NON_DELIVERY_OPTIONS = ("return_to_sender", "treat_as_abandoned")

# https://www.shipstation.com/developer-api/#/reference/stores/getupdate-store/update-store
UPDATE_STORE_OPTIONS = (
    "store_id",
    "store_name",
    "marketplace_id",
    "marketplace_name",
    "account_name",
    "email",
    "integration_url",
    "active",
    "company_name",
    "phone",
    "public_email",
    "website",
    "refresh_date",
    "last_refresh_attempt",
    "create_date",
    "modify_date",
    "auto_refresh",
    "status_mappings",
)

# https://www.shipstation.com/developer-api/#/reference/webhooks/subscribe-to-webhook/subscribe-to-webhook
SUBSCRIBE_TO_WEBHOOK_OPTIONS = ("target_url", "event", "store_id", "friendly_name")

# https://www.shipstation.com/developer-api/#/reference/webhooks/subscribe-to-webhook/subscribe-to-webhook
SUBSCRIBE_TO_WEBHOOK_EVENT_OPTIONS = (
    "ORDER_NOTIFY",
    "ITEM_ORDER_NOTIFY",
    "SHIP_NOTIFY",
    "ITEM_SHIP_NOTIFY",
)

WEIGHT_UNIT_OPTIONS = ("pounds", "ounces", "grams")

DIMENSIONS_UNIT_OPTIONS = ("inches", "centimeters")
