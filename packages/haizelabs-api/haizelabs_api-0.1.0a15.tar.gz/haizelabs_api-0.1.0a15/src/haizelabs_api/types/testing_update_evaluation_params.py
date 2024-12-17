# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["TestingUpdateEvaluationParams"]


class TestingUpdateEvaluationParams(TypedDict, total=False):
    eval_id: Required[str]

    status: Required[Literal["COMPLETE", "ERROR", "RUNNING", "STOPPED", "PENDING"]]

    user_id: Required[str]
