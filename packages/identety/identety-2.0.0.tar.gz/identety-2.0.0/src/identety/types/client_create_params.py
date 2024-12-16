# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientCreateParams"]


class ClientCreateParams(TypedDict, total=False):
    name: Required[str]
    """Client Name"""

    type: Required[Literal["public", "private", "m2m"]]
    """Client type"""

    allowed_grants: Annotated[
        List[Literal["authorization_code", "client_credentials", "refresh_token"]], PropertyInfo(alias="allowedGrants")
    ]
    """Allowed Grants"""

    allowed_scopes: Annotated[List[str], PropertyInfo(alias="allowedScopes")]
    """Allowed Scopes"""

    redirect_uris: Annotated[List[str], PropertyInfo(alias="redirectUris")]
    """Redirect URIs"""

    settings: object
    """Client Settings"""
