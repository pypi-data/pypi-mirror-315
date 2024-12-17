# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TestingUpdateEvaluationParams"]


class TestingUpdateEvaluationParams(TypedDict, total=False):
    eval_id: Required[str]

    status: Required[Literal["COMPLETE", "ERROR", "RUNNING", "STOPPED", "PENDING"]]

    user_id: Required[str]

    end_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    start_date: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
