# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["User", "Address"]


class Address(BaseModel):
    country: str

    locality: str

    postal_code: str = FieldInfo(alias="postalCode")

    region: str

    street_address: str = FieldInfo(alias="streetAddress")


class User(BaseModel):
    id: str

    address: Address

    family_name: str = FieldInfo(alias="familyName")

    given_name: str = FieldInfo(alias="givenName")

    locale: str

    metadata: object

    name: str

    picture: str
