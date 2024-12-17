# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TestingCreateEvaluationResponse"]


class TestingCreateEvaluationResponse(BaseModel):
    __test__ = False
    id: str

    status: Literal["COMPLETE", "ERROR", "RUNNING", "STOPPED", "PENDING"]
