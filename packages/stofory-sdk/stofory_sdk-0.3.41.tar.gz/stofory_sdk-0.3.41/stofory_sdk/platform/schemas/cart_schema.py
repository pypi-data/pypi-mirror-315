import enum
from typing import List

import msgspec

from stofory_sdk.catalog.models.enums import ParameterType, ModifierOperator, Currency
from stofory_sdk.digiseller.n2_payments.schemas import CartTypeCurrency


class OptionSchema(msgspec.Struct):
    option_id: int


class ParameterSchema(msgspec.Struct):
    parameter_id: int
    parameter_type: ParameterType
    value: str
    options: List[OptionSchema]


class CartProductSchema(msgspec.Struct):
    id: int
    name: str
    discount: int
    price: int
    total_price: int | None
    quantity: int
    unit_quantity: int | None
    payment_type: CartTypeCurrency
    parameters: List[ParameterSchema]


class CartCreateRequest(msgspec.Struct):
    email: str | None
    items: List[CartProductSchema]


class CartCreateResponse(msgspec.Struct):
    cart_id: str
    id_po: int | None
