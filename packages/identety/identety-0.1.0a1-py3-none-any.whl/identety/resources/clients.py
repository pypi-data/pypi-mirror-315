# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import client_list_params, client_create_params, client_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.client import Client
from ..types.client_list_response import ClientListResponse

__all__ = ["ClientsResource", "AsyncClientsResource"]


class ClientsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ClientsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/identety/identety-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ClientsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClientsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/identety/identety-python-sdk#with_streaming_response
        """
        return ClientsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        type: Literal["public", "private", "m2m"],
        allowed_grants: List[Literal["authorization_code", "client_credentials", "refresh_token"]]
        | NotGiven = NOT_GIVEN,
        allowed_scopes: List[str] | NotGiven = NOT_GIVEN,
        redirect_uris: List[str] | NotGiven = NOT_GIVEN,
        settings: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Create new client

        Args:
          name: Client Name

          type: Client type

          allowed_grants: Allowed Grants

          allowed_scopes: Allowed Scopes

          redirect_uris: Redirect URIs

          settings: Client Settings

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/clients",
            body=maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "allowed_grants": allowed_grants,
                    "allowed_scopes": allowed_scopes,
                    "redirect_uris": redirect_uris,
                    "settings": settings,
                },
                client_create_params.ClientCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Get client details by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/clients/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )

    def update(
        self,
        id: str,
        *,
        name: str,
        allowed_grants: List[Literal["authorization_code", "client_credentials", "refresh_token"]]
        | NotGiven = NOT_GIVEN,
        allowed_scopes: List[str] | NotGiven = NOT_GIVEN,
        redirect_uris: List[str] | NotGiven = NOT_GIVEN,
        settings: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Update client

        Args:
          name: Client Name

          allowed_grants: Allowed Grants

          allowed_scopes: Allowed Scopes

          redirect_uris: Redirect URIs

          settings: Client Settings

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/clients/{id}",
            body=maybe_transform(
                {
                    "name": name,
                    "allowed_grants": allowed_grants,
                    "allowed_scopes": allowed_scopes,
                    "redirect_uris": redirect_uris,
                    "settings": settings,
                },
                client_update_params.ClientUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )

    def list(
        self,
        *,
        columns: Literal[
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
        ],
        limit: float | NotGiven = NOT_GIVEN,
        page: float | NotGiven = NOT_GIVEN,
        sort: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        sort_by: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientListResponse:
        """
        Get all clients

        Args:
          columns: Comma separated column names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/clients",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "columns": columns,
                        "limit": limit,
                        "page": page,
                        "sort": sort,
                        "sort_by": sort_by,
                    },
                    client_list_params.ClientListParams,
                ),
            ),
            cast_to=ClientListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Delete client

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._delete(
            f"/clients/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )


class AsyncClientsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncClientsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/identety/identety-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncClientsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClientsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/identety/identety-python-sdk#with_streaming_response
        """
        return AsyncClientsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        type: Literal["public", "private", "m2m"],
        allowed_grants: List[Literal["authorization_code", "client_credentials", "refresh_token"]]
        | NotGiven = NOT_GIVEN,
        allowed_scopes: List[str] | NotGiven = NOT_GIVEN,
        redirect_uris: List[str] | NotGiven = NOT_GIVEN,
        settings: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Create new client

        Args:
          name: Client Name

          type: Client type

          allowed_grants: Allowed Grants

          allowed_scopes: Allowed Scopes

          redirect_uris: Redirect URIs

          settings: Client Settings

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/clients",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "type": type,
                    "allowed_grants": allowed_grants,
                    "allowed_scopes": allowed_scopes,
                    "redirect_uris": redirect_uris,
                    "settings": settings,
                },
                client_create_params.ClientCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Get client details by id

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/clients/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )

    async def update(
        self,
        id: str,
        *,
        name: str,
        allowed_grants: List[Literal["authorization_code", "client_credentials", "refresh_token"]]
        | NotGiven = NOT_GIVEN,
        allowed_scopes: List[str] | NotGiven = NOT_GIVEN,
        redirect_uris: List[str] | NotGiven = NOT_GIVEN,
        settings: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Update client

        Args:
          name: Client Name

          allowed_grants: Allowed Grants

          allowed_scopes: Allowed Scopes

          redirect_uris: Redirect URIs

          settings: Client Settings

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/clients/{id}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "allowed_grants": allowed_grants,
                    "allowed_scopes": allowed_scopes,
                    "redirect_uris": redirect_uris,
                    "settings": settings,
                },
                client_update_params.ClientUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )

    async def list(
        self,
        *,
        columns: Literal[
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
        ],
        limit: float | NotGiven = NOT_GIVEN,
        page: float | NotGiven = NOT_GIVEN,
        sort: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        sort_by: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ClientListResponse:
        """
        Get all clients

        Args:
          columns: Comma separated column names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/clients",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "columns": columns,
                        "limit": limit,
                        "page": page,
                        "sort": sort,
                        "sort_by": sort_by,
                    },
                    client_list_params.ClientListParams,
                ),
            ),
            cast_to=ClientListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Client:
        """
        Delete client

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._delete(
            f"/clients/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Client,
        )


class ClientsResourceWithRawResponse:
    def __init__(self, clients: ClientsResource) -> None:
        self._clients = clients

        self.create = to_raw_response_wrapper(
            clients.create,
        )
        self.retrieve = to_raw_response_wrapper(
            clients.retrieve,
        )
        self.update = to_raw_response_wrapper(
            clients.update,
        )
        self.list = to_raw_response_wrapper(
            clients.list,
        )
        self.delete = to_raw_response_wrapper(
            clients.delete,
        )


class AsyncClientsResourceWithRawResponse:
    def __init__(self, clients: AsyncClientsResource) -> None:
        self._clients = clients

        self.create = async_to_raw_response_wrapper(
            clients.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            clients.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            clients.update,
        )
        self.list = async_to_raw_response_wrapper(
            clients.list,
        )
        self.delete = async_to_raw_response_wrapper(
            clients.delete,
        )


class ClientsResourceWithStreamingResponse:
    def __init__(self, clients: ClientsResource) -> None:
        self._clients = clients

        self.create = to_streamed_response_wrapper(
            clients.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            clients.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            clients.update,
        )
        self.list = to_streamed_response_wrapper(
            clients.list,
        )
        self.delete = to_streamed_response_wrapper(
            clients.delete,
        )


class AsyncClientsResourceWithStreamingResponse:
    def __init__(self, clients: AsyncClientsResource) -> None:
        self._clients = clients

        self.create = async_to_streamed_response_wrapper(
            clients.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            clients.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            clients.update,
        )
        self.list = async_to_streamed_response_wrapper(
            clients.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            clients.delete,
        )
