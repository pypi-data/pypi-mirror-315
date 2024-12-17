# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["TestingWriteScoreParams", "JudgeResult"]


class TestingWriteScoreParams(TypedDict, total=False):
    judge_result: Required[JudgeResult]

    span_id: Required[str]


class JudgeResult(TypedDict, total=False):
    judge_id: Required[str]

    score: Required[float]

    judge_name: Optional[str]

    label: Optional[str]
