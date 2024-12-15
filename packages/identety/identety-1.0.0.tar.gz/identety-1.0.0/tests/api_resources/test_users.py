# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from identety import Identety, AsyncIdentety
from tests.utils import assert_matches_type
from identety.types import User, UserListResponse

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
        assert_matches_type(User, user, path=["response"])

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
        assert_matches_type(User, user, path=["response"])

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
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Identety) -> None:
        user = client.users.retrieve(
            "id",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Identety) -> None:
        response = client.users.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Identety) -> None:
        with client.users.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Identety) -> None:
        user = client.users.update(
            id="id",
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            picture="https://example.com/photo.jpg",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Identety) -> None:
        response = client.users.with_raw_response.update(
            id="id",
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            picture="https://example.com/photo.jpg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Identety) -> None:
        with client.users.with_streaming_response.update(
            id="id",
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            picture="https://example.com/photo.jpg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.update(
                id="",
                address={
                    "country": "USA",
                    "locality": "New York",
                    "postal_code": "10001",
                    "region": "NY",
                    "street_address": "123 Main St",
                },
                family_name="Doe",
                given_name="John",
                locale="en-US",
                metadata={"customField": "value"},
                name="John Doe",
                picture="https://example.com/photo.jpg",
            )

    @parametrize
    def test_method_list(self, client: Identety) -> None:
        user = client.users.list(
            columns="id",
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Identety) -> None:
        user = client.users.list(
            columns="id",
            limit=0,
            page=0,
            sort="asc",
            sort_by="sortBy",
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Identety) -> None:
        response = client.users.with_raw_response.list(
            columns="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Identety) -> None:
        with client.users.with_streaming_response.list(
            columns="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserListResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Identety) -> None:
        user = client.users.delete(
            "id",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Identety) -> None:
        response = client.users.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Identety) -> None:
        with client.users.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.delete(
                "",
            )


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
        assert_matches_type(User, user, path=["response"])

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
        assert_matches_type(User, user, path=["response"])

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
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIdentety) -> None:
        user = await async_client.users.retrieve(
            "id",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIdentety) -> None:
        response = await async_client.users.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIdentety) -> None:
        async with async_client.users.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncIdentety) -> None:
        user = await async_client.users.update(
            id="id",
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            picture="https://example.com/photo.jpg",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncIdentety) -> None:
        response = await async_client.users.with_raw_response.update(
            id="id",
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            picture="https://example.com/photo.jpg",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncIdentety) -> None:
        async with async_client.users.with_streaming_response.update(
            id="id",
            address={
                "country": "USA",
                "locality": "New York",
                "postal_code": "10001",
                "region": "NY",
                "street_address": "123 Main St",
            },
            family_name="Doe",
            given_name="John",
            locale="en-US",
            metadata={"customField": "value"},
            name="John Doe",
            picture="https://example.com/photo.jpg",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.update(
                id="",
                address={
                    "country": "USA",
                    "locality": "New York",
                    "postal_code": "10001",
                    "region": "NY",
                    "street_address": "123 Main St",
                },
                family_name="Doe",
                given_name="John",
                locale="en-US",
                metadata={"customField": "value"},
                name="John Doe",
                picture="https://example.com/photo.jpg",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncIdentety) -> None:
        user = await async_client.users.list(
            columns="id",
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncIdentety) -> None:
        user = await async_client.users.list(
            columns="id",
            limit=0,
            page=0,
            sort="asc",
            sort_by="sortBy",
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncIdentety) -> None:
        response = await async_client.users.with_raw_response.list(
            columns="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserListResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncIdentety) -> None:
        async with async_client.users.with_streaming_response.list(
            columns="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserListResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncIdentety) -> None:
        user = await async_client.users.delete(
            "id",
        )
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncIdentety) -> None:
        response = await async_client.users.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(User, user, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncIdentety) -> None:
        async with async_client.users.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(User, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.delete(
                "",
            )
