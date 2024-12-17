# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, overload

import httpx

from ..types import monitoring_log_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    required_args,
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

__all__ = ["MonitoringResource", "AsyncMonitoringResource"]


class MonitoringResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MonitoringResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#accessing-raw-response-data-eg-headers
        """
        return MonitoringResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MonitoringResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#with_streaming_response
        """
        return MonitoringResourceWithStreamingResponse(self)

    @overload
    def log(
        self,
        *,
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        caller_id: Optional[str] | NotGiven = NOT_GIVEN,
        end: Union[str, datetime] | NotGiven = NOT_GIVEN,
        eval_id: str | NotGiven = NOT_GIVEN,
        inputs: object | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        outputs: object | NotGiven = NOT_GIVEN,
        parent_id: Optional[str] | NotGiven = NOT_GIVEN,
        scores: Iterable[monitoring_log_params.SpanScore] | NotGiven = NOT_GIVEN,
        span_type: Optional[Literal["DETECTOR", "JUDGE", "APP", "MODEL", "FUNCTION", "SCORER"]] | NotGiven = NOT_GIVEN,
        start: Union[str, datetime] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        logs a span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def log(
        self,
        *,
        root_span: str,
        id: str | NotGiven = NOT_GIVEN,
        end: Union[str, datetime] | NotGiven = NOT_GIVEN,
        eval_id: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        start: Union[str, datetime] | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        logs a span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["trace_id"], ["root_span"])
    def log(
        self,
        *,
        trace_id: str | NotGiven = NOT_GIVEN,
        id: str | NotGiven = NOT_GIVEN,
        caller_id: Optional[str] | NotGiven = NOT_GIVEN,
        end: Union[str, datetime] | NotGiven = NOT_GIVEN,
        eval_id: str | NotGiven = NOT_GIVEN,
        inputs: object | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        outputs: object | NotGiven = NOT_GIVEN,
        parent_id: Optional[str] | NotGiven = NOT_GIVEN,
        scores: Iterable[monitoring_log_params.SpanScore] | NotGiven = NOT_GIVEN,
        span_type: Optional[Literal["DETECTOR", "JUDGE", "APP", "MODEL", "FUNCTION", "SCORER"]] | NotGiven = NOT_GIVEN,
        start: Union[str, datetime] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        root_span: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        return self._post(
            "/monitoring/log",
            body=maybe_transform(
                {
                    "trace_id": trace_id,
                    "id": id,
                    "caller_id": caller_id,
                    "end": end,
                    "eval_id": eval_id,
                    "inputs": inputs,
                    "metadata": metadata,
                    "name": name,
                    "outputs": outputs,
                    "parent_id": parent_id,
                    "scores": scores,
                    "span_type": span_type,
                    "start": start,
                    "tags": tags,
                    "user_id": user_id,
                    "root_span": root_span,
                },
                monitoring_log_params.MonitoringLogParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncMonitoringResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMonitoringResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMonitoringResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMonitoringResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/haizelabs/haizelabs-python#with_streaming_response
        """
        return AsyncMonitoringResourceWithStreamingResponse(self)

    @overload
    async def log(
        self,
        *,
        trace_id: str,
        id: str | NotGiven = NOT_GIVEN,
        caller_id: Optional[str] | NotGiven = NOT_GIVEN,
        end: Union[str, datetime] | NotGiven = NOT_GIVEN,
        eval_id: str | NotGiven = NOT_GIVEN,
        inputs: object | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        outputs: object | NotGiven = NOT_GIVEN,
        parent_id: Optional[str] | NotGiven = NOT_GIVEN,
        scores: Iterable[monitoring_log_params.SpanScore] | NotGiven = NOT_GIVEN,
        span_type: Optional[Literal["DETECTOR", "JUDGE", "APP", "MODEL", "FUNCTION", "SCORER"]] | NotGiven = NOT_GIVEN,
        start: Union[str, datetime] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        logs a span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def log(
        self,
        *,
        root_span: str,
        id: str | NotGiven = NOT_GIVEN,
        end: Union[str, datetime] | NotGiven = NOT_GIVEN,
        eval_id: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        start: Union[str, datetime] | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        logs a span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["trace_id"], ["root_span"])
    async def log(
        self,
        *,
        trace_id: str | NotGiven = NOT_GIVEN,
        id: str | NotGiven = NOT_GIVEN,
        caller_id: Optional[str] | NotGiven = NOT_GIVEN,
        end: Union[str, datetime] | NotGiven = NOT_GIVEN,
        eval_id: str | NotGiven = NOT_GIVEN,
        inputs: object | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        outputs: object | NotGiven = NOT_GIVEN,
        parent_id: Optional[str] | NotGiven = NOT_GIVEN,
        scores: Iterable[monitoring_log_params.SpanScore] | NotGiven = NOT_GIVEN,
        span_type: Optional[Literal["DETECTOR", "JUDGE", "APP", "MODEL", "FUNCTION", "SCORER"]] | NotGiven = NOT_GIVEN,
        start: Union[str, datetime] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        root_span: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        return await self._post(
            "/monitoring/log",
            body=await async_maybe_transform(
                {
                    "trace_id": trace_id,
                    "id": id,
                    "caller_id": caller_id,
                    "end": end,
                    "eval_id": eval_id,
                    "inputs": inputs,
                    "metadata": metadata,
                    "name": name,
                    "outputs": outputs,
                    "parent_id": parent_id,
                    "scores": scores,
                    "span_type": span_type,
                    "start": start,
                    "tags": tags,
                    "user_id": user_id,
                    "root_span": root_span,
                },
                monitoring_log_params.MonitoringLogParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class MonitoringResourceWithRawResponse:
    def __init__(self, monitoring: MonitoringResource) -> None:
        self._monitoring = monitoring

        self.log = to_raw_response_wrapper(
            monitoring.log,
        )


class AsyncMonitoringResourceWithRawResponse:
    def __init__(self, monitoring: AsyncMonitoringResource) -> None:
        self._monitoring = monitoring

        self.log = async_to_raw_response_wrapper(
            monitoring.log,
        )


class MonitoringResourceWithStreamingResponse:
    def __init__(self, monitoring: MonitoringResource) -> None:
        self._monitoring = monitoring

        self.log = to_streamed_response_wrapper(
            monitoring.log,
        )


class AsyncMonitoringResourceWithStreamingResponse:
    def __init__(self, monitoring: AsyncMonitoringResource) -> None:
        self._monitoring = monitoring

        self.log = async_to_streamed_response_wrapper(
            monitoring.log,
        )
