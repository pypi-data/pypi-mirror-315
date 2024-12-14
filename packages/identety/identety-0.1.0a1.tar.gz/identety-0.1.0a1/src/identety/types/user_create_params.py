# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["UserCreateParams", "Address"]


class UserCreateParams(TypedDict, total=False):
    address: Required[Address]

    email: Required[str]

    family_name: Required[Annotated[str, PropertyInfo(alias="familyName")]]

    given_name: Required[Annotated[str, PropertyInfo(alias="givenName")]]

    locale: Required[str]

    metadata: Required[object]

    name: Required[str]

    password: Required[str]

    picture: Required[str]


class Address(TypedDict, total=False):
    country: Required[str]

    locality: Required[str]

    postal_code: Required[Annotated[str, PropertyInfo(alias="postalCode")]]

    region: Required[str]

    street_address: Required[Annotated[str, PropertyInfo(alias="streetAddress")]]
