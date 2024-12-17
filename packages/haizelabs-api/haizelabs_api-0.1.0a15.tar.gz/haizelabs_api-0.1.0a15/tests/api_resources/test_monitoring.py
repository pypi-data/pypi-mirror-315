# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from haizelabs_api import HaizeLabs, AsyncHaizeLabs
from haizelabs_api._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMonitoring:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_log_overload_1(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            trace_id="trace_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_method_log_with_all_params_overload_1(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            trace_id="trace_id",
            id="id",
            caller_id="caller_id",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            eval_id="eval_id",
            inputs={},
            metadata={},
            name="name",
            outputs={},
            parent_id="parent_id",
            scores=[
                {
                    "judge_id": "judge_id",
                    "score": 0,
                    "judge_name": "judge_name",
                    "label": "label",
                }
            ],
            span_type="DETECTOR",
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            tags={},
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_raw_response_log_overload_1(self, client: HaizeLabs) -> None:
        response = client.monitoring.with_raw_response.log(
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_streaming_response_log_overload_1(self, client: HaizeLabs) -> None:
        with client.monitoring.with_streaming_response.log(
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_log_overload_2(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            root_span="root_span",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_method_log_with_all_params_overload_2(self, client: HaizeLabs) -> None:
        monitoring = client.monitoring.log(
            root_span="root_span",
            id="id",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            eval_id="eval_id",
            name="name",
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_raw_response_log_overload_2(self, client: HaizeLabs) -> None:
        response = client.monitoring.with_raw_response.log(
            root_span="root_span",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    def test_streaming_response_log_overload_2(self, client: HaizeLabs) -> None:
        with client.monitoring.with_streaming_response.log(
            root_span="root_span",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncMonitoring:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_log_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            trace_id="trace_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_method_log_with_all_params_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            trace_id="trace_id",
            id="id",
            caller_id="caller_id",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            eval_id="eval_id",
            inputs={},
            metadata={},
            name="name",
            outputs={},
            parent_id="parent_id",
            scores=[
                {
                    "judge_id": "judge_id",
                    "score": 0,
                    "judge_name": "judge_name",
                    "label": "label",
                }
            ],
            span_type="DETECTOR",
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            tags={},
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_raw_response_log_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.monitoring.with_raw_response.log(
            trace_id="trace_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = await response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_streaming_response_log_overload_1(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.monitoring.with_streaming_response.log(
            trace_id="trace_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = await response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_log_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            root_span="root_span",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_method_log_with_all_params_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        monitoring = await async_client.monitoring.log(
            root_span="root_span",
            id="id",
            end=parse_datetime("2019-12-27T18:11:19.117Z"),
            eval_id="eval_id",
            name="name",
            start=parse_datetime("2019-12-27T18:11:19.117Z"),
            user_id="user_id",
        )
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_raw_response_log_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        response = await async_client.monitoring.with_raw_response.log(
            root_span="root_span",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        monitoring = await response.parse()
        assert_matches_type(object, monitoring, path=["response"])

    @parametrize
    async def test_streaming_response_log_overload_2(self, async_client: AsyncHaizeLabs) -> None:
        async with async_client.monitoring.with_streaming_response.log(
            root_span="root_span",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            monitoring = await response.parse()
            assert_matches_type(object, monitoring, path=["response"])

        assert cast(Any, response.is_closed) is True
