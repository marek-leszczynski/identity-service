from enum import Enum


class HealthCheckStatus(str, Enum):
    OK = "ok"
    FAILED = "failed"


class HealthCheckGroup(str, Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
