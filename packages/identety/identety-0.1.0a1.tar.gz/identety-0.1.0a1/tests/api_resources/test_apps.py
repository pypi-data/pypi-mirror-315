# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from identety import Identety, AsyncIdentety

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApps:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Identety) -> None:
        app = client.apps.retrieve()
        assert app is None

    @parametrize
    def test_raw_response_retrieve(self, client: Identety) -> None:
        response = client.apps.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = response.parse()
        assert app is None

    @parametrize
    def test_streaming_response_retrieve(self, client: Identety) -> None:
        with client.apps.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = response.parse()
            assert app is None

        assert cast(Any, response.is_closed) is True


class TestAsyncApps:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncIdentety) -> None:
        app = await async_client.apps.retrieve()
        assert app is None

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncIdentety) -> None:
        response = await async_client.apps.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        app = await response.parse()
        assert app is None

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncIdentety) -> None:
        async with async_client.apps.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            app = await response.parse()
            assert app is None

        assert cast(Any, response.is_closed) is True
