# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .user import User
from .._models import BaseModel

__all__ = ["UserListResponse"]


class UserListResponse(BaseModel):
    meta: object

    nodes: List[User]
