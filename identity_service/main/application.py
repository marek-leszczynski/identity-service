import logging
import typing as T
from json import JSONDecodeError

from fastapi import FastAPI as FastAPIBase
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from ..settings import settings
from .api import router
from .models import ErrorResponseContent
from .responses import ErrorResponse

logger = logging.getLogger(__name__)


class FastAPI(FastAPIBase):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.add_exception_handler(
            RequestValidationError, self._validation_error_handler
        )
        self.add_exception_handler(HTTPException, self._api_exception_handler)
        self.add_exception_handler(Exception, self._unhandled_exception_handler)

    @staticmethod
    def _get_error_response(
        exc: Exception,
        status_code: int,
        detail: str,
        errors: T.Optional[T.List[dict]] = None,
    ) -> ErrorResponse:
        return ErrorResponse(
            status_code=status_code,
            content=ErrorResponseContent(
                title=str(exc.__class__.__name__),
                status=status_code,
                detail=detail,
                errors=jsonable_encoder(errors),
            ).dict(),
        )

    async def _validation_error_handler(
        self, _: Request, exc: RequestValidationError
    ) -> ErrorResponse:
        raw_exception = exc.raw_errors[0].exc  # type: ignore
        if isinstance(raw_exception, JSONDecodeError):
            return self._get_error_response(
                raw_exception,
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(raw_exception),
            )
        return self._get_error_response(
            exc,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request could not be processed due to a validation error.",
            errors=exc.errors(),  # type: ignore
        )

    async def _api_exception_handler(
        self, _: Request, exc: HTTPException
    ) -> ErrorResponse:
        logger.exception("API exception.")
        return self._get_error_response(
            exc, status_code=exc.status_code, detail=str(exc.detail)
        )

    async def _unhandled_exception_handler(
        self, _: Request, exc: Exception
    ) -> ErrorResponse:
        logger.exception("Unhandled exception.")
        return self._get_error_response(
            exc,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )


app = FastAPI(title="Authentication Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
