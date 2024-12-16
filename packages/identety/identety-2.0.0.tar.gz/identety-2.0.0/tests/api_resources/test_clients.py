# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from identety import Identety, AsyncIdentety
from tests.utils import assert_matches_type
from identety.types import Client, ClientListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClients:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Identety) -> None:
        client_ = client.clients.create(
            name="name",
            type="public",
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Identety) -> None:
        client_ = client.clients.create(
            name="name",
            type="public",
            allowed_grants=["authorization_code"],
            allowed_scopes=["string"],
            redirect_uris=["string"],
            settings={},
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Identety) -> None:
        response = client.clients.with_raw_response.create(
            name="name",
            type="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Identety) -> None:
        with client.clients.with_streaming_response.create(
            name="name",
            type="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(Client, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Identety) -> None:
        client_ = client.clients.retrieve(
            "id",
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Identety) -> None:
        response = client.clients.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Identety) -> None:
        with client.clients.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(Client, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.clients.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Identety) -> None:
        client_ = client.clients.update(
            id="id",
            name="name",
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Identety) -> None:
        client_ = client.clients.update(
            id="id",
            name="name",
            allowed_grants=["authorization_code"],
            allowed_scopes=["string"],
            redirect_uris=["string"],
            settings={},
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Identety) -> None:
        response = client.clients.with_raw_response.update(
            id="id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Identety) -> None:
        with client.clients.with_streaming_response.update(
            id="id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(Client, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.clients.with_raw_response.update(
                id="",
                name="name",
            )

    @parametrize
    def test_method_list(self, client: Identety) -> None:
        client_ = client.clients.list(
            columns="id",
        )
        assert_matches_type(ClientListResponse, client_, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Identety) -> None:
        client_ = client.clients.list(
            columns="id",
            limit=0,
            page=0,
            sort="asc",
            sort_by="sortBy",
        )
        assert_matches_type(ClientListResponse, client_, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Identety) -> None:
        response = client.clients.with_raw_response.list(
            columns="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ClientListResponse, client_, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Identety) -> None:
        with client.clients.with_streaming_response.list(
            columns="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ClientListResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Identety) -> None:
        client_ = client.clients.delete(
            "id",
        )
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Identety) -> None:
        response = client.clients.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(Client, client_, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Identety) -> None:
        with client.clients.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(Client, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.clients.with_raw_response.delete(
                "",
            )


class TestAsyncClients:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.create(
            name="name",
            type="public",
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.create(
            name="name",
            type="public",
            allowed_grants=["authorization_code"],
            allowed_scopes=["string"],
            redirect_uris=["string"],
            settings={},
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncIdentety) -> None:
        response = await async_client.clients.with_raw_response.create(
            name="name",
            type="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncIdentety) -> None:
        async with async_client.clients.with_streaming_response.create(
            name="name",
            type="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(Client, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.retrieve(
            "id",
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIdentety) -> None:
        response = await async_client.clients.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIdentety) -> None:
        async with async_client.clients.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(Client, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.clients.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.update(
            id="id",
            name="name",
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.update(
            id="id",
            name="name",
            allowed_grants=["authorization_code"],
            allowed_scopes=["string"],
            redirect_uris=["string"],
            settings={},
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncIdentety) -> None:
        response = await async_client.clients.with_raw_response.update(
            id="id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncIdentety) -> None:
        async with async_client.clients.with_streaming_response.update(
            id="id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(Client, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.clients.with_raw_response.update(
                id="",
                name="name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.list(
            columns="id",
        )
        assert_matches_type(ClientListResponse, client, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.list(
            columns="id",
            limit=0,
            page=0,
            sort="asc",
            sort_by="sortBy",
        )
        assert_matches_type(ClientListResponse, client, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncIdentety) -> None:
        response = await async_client.clients.with_raw_response.list(
            columns="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ClientListResponse, client, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncIdentety) -> None:
        async with async_client.clients.with_streaming_response.list(
            columns="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ClientListResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncIdentety) -> None:
        client = await async_client.clients.delete(
            "id",
        )
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncIdentety) -> None:
        response = await async_client.clients.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(Client, client, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncIdentety) -> None:
        async with async_client.clients.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(Client, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.clients.with_raw_response.delete(
                "",
            )
