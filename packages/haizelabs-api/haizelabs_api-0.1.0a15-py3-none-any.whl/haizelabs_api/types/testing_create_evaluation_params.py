# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["TestingCreateEvaluationParams"]


class TestingCreateEvaluationParams(TypedDict, total=False):
    eval_type: Required[Literal["EVALUATION", "FUZZING", "RED_TEAMING"]]

    name: Required[str]

    user_id: Required[str]
