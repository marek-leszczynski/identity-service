import asyncio
import logging
import time
import typing as T
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import db_session
from .health_checks import (
    FastAPIHealthCheck,
    HealthCheck,
    SQLAlchemyDatabaseHealthCheck,
)
from .models import HealthCheckStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health-checks")


@router.get(
    "/simple",
    response_class=Response,
    name="Simple Health Check",
    description="Checks if FastAPI HTTP server is up and running",
    status_code=HTTPStatus.OK,
)
async def simple_health_check() -> Response:
    return await _run_health_checks([FastAPIHealthCheck()])


@router.get(
    "/complex",
    response_class=Response,
    name="Complex Health Check",
    description=(
        "Checks if the FastAPI HTTP server is up and running and if the service "
        "can reach all its dependent services"
    ),
    status_code=HTTPStatus.OK,
)
async def complex_health_check(session: Session = Depends(db_session)) -> Response:
    return await _run_health_checks(
        [FastAPIHealthCheck(), SQLAlchemyDatabaseHealthCheck(session)]
    )


async def _run_health_checks(health_checks: T.List[HealthCheck]) -> Response:
    start_time = time.time()
    results = await asyncio.gather(
        *[health_check.run() for health_check in health_checks]
    )
    total_execution_time = round(time.time() - start_time, 4)
    failed_health_checks = []
    logging_extra: dict = {
        "total_execution_time": total_execution_time,
        "results": [],
    }
    for result in results:
        if result.status == HealthCheckStatus.FAILED:
            failed_health_checks.append(result)
        logging_extra["results"].append(result.dict())

    if failed_health_checks:
        logger.warning(
            "Following health checks have failed: %s",
            [f"{check.type}: {check.target}" for check in failed_health_checks],
            extra=logging_extra,
        )
        raise HTTPException(status_code=HTTPStatus.FAILED_DEPENDENCY)
    logging.info("All health checks have passed", extra=logging_extra)
    return Response("OK")
