# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientListParams"]


class ClientListParams(TypedDict, total=False):
    columns: Required[
        Literal[
            "id",
            "client_id",
            "client_secret",
            "name",
            "type",
            "redirect_uris",
            "allowed_scopes",
            "allowed_grants",
            "is_active",
            "require_pkce",
            "settings",
            "tenant_id",
            "created_at",
            "updated_at",
        ]
    ]
    """Comma separated column names"""

    limit: float

    page: float

    sort: Literal["asc", "desc"]

    sort_by: Annotated[str, PropertyInfo(alias="sortBy")]
