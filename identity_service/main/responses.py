from fastapi.responses import JSONResponse


class ErrorResponse(JSONResponse):
    media_type = "application/problem+json"
