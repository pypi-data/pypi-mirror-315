# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["MonitoringLogParams", "Span", "SpanScore", "Trace"]


class Span(TypedDict, total=False):
    trace_id: Required[str]

    id: str

    caller_id: Optional[str]

    end: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    eval_id: str

    inputs: object

    metadata: object

    name: str

    outputs: object

    parent_id: Optional[str]

    scores: Iterable[SpanScore]

    span_type: Optional[Literal["DETECTOR", "JUDGE", "APP", "MODEL", "FUNCTION", "SCORER"]]

    start: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    tags: object

    user_id: str


class SpanScore(TypedDict, total=False):
    judge_id: Required[str]

    score: Required[float]

    judge_name: Optional[str]

    label: Optional[str]


class Trace(TypedDict, total=False):
    root_span: Required[str]

    id: str

    end: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    eval_id: str

    name: str

    start: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    user_id: str


MonitoringLogParams: TypeAlias = Union[Span, Trace]
