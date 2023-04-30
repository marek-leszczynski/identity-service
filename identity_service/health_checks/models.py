import typing as T

from pydantic import BaseModel

from .enums import HealthCheckStatus


class HealthCheckResult(BaseModel):
    type: str
    target: T.Optional[str]
    status: HealthCheckStatus
    error: T.Optional[str]
    execution_time: float
