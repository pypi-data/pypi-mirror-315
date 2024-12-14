# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from identety import Identety, AsyncIdentety

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRoles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Identety) -> None:
        role = client.roles.retrieve(
            "id",
        )
        assert role is None

    @parametrize
    def test_raw_response_retrieve(self, client: Identety) -> None:
        response = client.roles.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        role = response.parse()
        assert role is None

    @parametrize
    def test_streaming_response_retrieve(self, client: Identety) -> None:
        with client.roles.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            role = response.parse()
            assert role is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Identety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.roles.with_raw_response.retrieve(
                "",
            )


class TestAsyncRoles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIdentety) -> None:
        role = await async_client.roles.retrieve(
            "id",
        )
        assert role is None

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIdentety) -> None:
        response = await async_client.roles.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        role = await response.parse()
        assert role is None

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIdentety) -> None:
        async with async_client.roles.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            role = await response.parse()
            assert role is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncIdentety) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.roles.with_raw_response.retrieve(
                "",
            )
