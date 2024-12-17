# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TestingCreateEvaluationParams"]


class TestingCreateEvaluationParams(TypedDict, total=False):
    eval_type: Required[Literal["EVALUATION", "FUZZING", "RED_TEAMING"]]

    name: Required[str]

    start_date: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    user_id: Required[str]
