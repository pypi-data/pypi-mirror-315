# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Client"]


class Client(BaseModel):
    id: str

    allowed_grants: List[str] = FieldInfo(alias="allowedGrants")

    allowed_scopes: List[str] = FieldInfo(alias="allowedScopes")

    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    is_active: bool = FieldInfo(alias="isActive")

    name: str

    redirect_uris: List[str] = FieldInfo(alias="redirectUris")

    settings: object

    type: Literal["public", "private", "m2m"]
