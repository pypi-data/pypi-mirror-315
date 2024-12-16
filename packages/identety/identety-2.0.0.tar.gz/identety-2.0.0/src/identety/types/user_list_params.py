# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["UserListParams"]


class UserListParams(TypedDict, total=False):
    columns: Required[
        Literal[
            "id",
            "email",
            "name",
            "phone_number",
            "address",
            "locale",
            "email_verified",
            "phone_number_verified",
            "created_at",
            "updated_at",
        ]
    ]
    """Comma separated column names"""

    limit: float

    page: float

    sort: Literal["asc", "desc"]

    sort_by: Annotated[str, PropertyInfo(alias="sortBy")]
