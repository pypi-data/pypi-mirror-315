# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .misc.country_code import CountryCode

__all__ = ["SubscriptionCreateParams", "Billing", "Customer"]


class SubscriptionCreateParams(TypedDict, total=False):
    billing: Required[Billing]

    customer: Required[Customer]

    product_id: Required[str]

    quantity: Required[int]

    payment_link: Optional[bool]
    """False by default"""

    return_url: Optional[str]


class Billing(TypedDict, total=False):
    city: Required[str]

    country: Required[CountryCode]
    """ISO country code alpha2 variant"""

    state: Required[str]

    street: Required[str]

    zipcode: Required[int]


class Customer(TypedDict, total=False):
    email: Required[str]

    name: Required[str]

    phone_number: Optional[str]
