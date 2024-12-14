# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .client import Client
from .._models import BaseModel

__all__ = ["ClientListResponse"]


class ClientListResponse(BaseModel):
    meta: object

    nodes: List[Client]
