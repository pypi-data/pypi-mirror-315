# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from identety import Identety, AsyncIdentety

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Identety) -> None:
        user = client.users.create(
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            email="john@example.com",
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            password="password123",
            picture="https://example.com/photo.jpg",
        )
        assert user is None

    @parametrize
    def test_raw_response_create(self, client: Identety) -> None:
        response = client.users.with_raw_response.create(
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            email="john@example.com",
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            password="password123",
            picture="https://example.com/photo.jpg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert user is None

    @parametrize
    def test_streaming_response_create(self, client: Identety) -> None:
        with client.users.with_streaming_response.create(
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            email="john@example.com",
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            password="password123",
            picture="https://example.com/photo.jpg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncIdentety) -> None:
        user = await async_client.users.create(
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            email="john@example.com",
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            password="password123",
            picture="https://example.com/photo.jpg",
        )
        assert user is None

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncIdentety) -> None:
        response = await async_client.users.with_raw_response.create(
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            email="john@example.com",
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            password="password123",
            picture="https://example.com/photo.jpg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert user is None

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncIdentety) -> None:
        async with async_client.users.with_streaming_response.create(
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            email="john@example.com",
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            password="password123",
            picture="https://example.com/photo.jpg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True
