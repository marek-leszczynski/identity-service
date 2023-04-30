import abc
import logging
import time
import typing as T
import uuid

import aiohttp
from pydantic import UUID4, AnyHttpUrl
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .enums import HealthCheckGroup, HealthCheckStatus
from .models import HealthCheckResult
from .schemas import HealthCheck as HealthCheckSchema

logger = logging.getLogger(__name__)


class HealthCheck(abc.ABC):
    _target: T.Optional[str] = None
    group: HealthCheckGroup

    @abc.abstractmethod
    async def _run(self) -> None:
        raise NotImplementedError

    def __init_subclass__(cls, group: HealthCheckGroup) -> None:
        cls.group = group

    def _compile_result(
        self, status: HealthCheckStatus, execution_time: float, error: T.Optional[str]
    ) -> HealthCheckResult:
        result = HealthCheckResult(
            type=self.__class__.__name__,
            target=self._target,
            error=error,
            status=status,
            execution_time=round(execution_time, 4),
        )
        logger.info(
            "%s %s for %s",
            result.type,
            result.status.value,
            result.target,
            extra={"execution_time": execution_time, "error": result.error},
        )
        return result

    async def run(self) -> HealthCheckResult:
        logger.info("Running %s for %s", self.__class__.__name__, self._target)
        start_time = time.time()
        error = None
        try:
            await self._run()
        except Exception as exc:  # pylint: disable=broad-except
            status = HealthCheckStatus.FAILED
            error = str(exc)
        else:
            status = HealthCheckStatus.OK

        return self._compile_result(
            status=status, execution_time=time.time() - start_time, error=error
        )


class FastAPIHealthCheck(HealthCheck, group=HealthCheckGroup.SIMPLE):
    async def _run(self) -> None:
        ...


class HTTPHealthCheck(HealthCheck, group=HealthCheckGroup.COMPLEX):
    def __init__(
        self,
        url: AnyHttpUrl,
        headers: T.Optional[dict] = None,
        callback: T.Optional[T.Callable] = None,
    ) -> None:
        self._url = url
        self._target = self._url
        self._headers = headers
        self._callback = callback

    async def _run(self) -> None:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(10), headers=self._headers
        ) as session:
            async with session.get(self._url) as response:
                if self._callback is not None:
                    await self._callback(response)
                else:
                    response.raise_for_status()


class SQLAlchemyDatabaseHealthCheck(HealthCheck, group=HealthCheckGroup.COMPLEX):
    def __init__(self, session: Session) -> None:
        self._session = session
        url = T.cast(Engine, session.bind).url
        self._target = f"{url.host}:{url.port}/{url.database}"

    def _insert_record(self, health_check_id: UUID4) -> None:
        self._session.add(HealthCheckSchema(id=health_check_id))  # type: ignore[call-arg]

    def _get_record(self, health_check_id: UUID4) -> None:
        self._session.query(HealthCheckSchema).filter(
            HealthCheckSchema.id == health_check_id
        ).one()

    def _delete_record(self, health_check_id: UUID4) -> None:
        self._session.query(HealthCheckSchema).filter(
            HealthCheckSchema.id == health_check_id
        ).delete()

    async def _run(self) -> None:
        health_check_id = uuid.uuid4()
        self._insert_record(health_check_id)
        self._get_record(health_check_id)
        self._delete_record(health_check_id)
        self._session.commit()
