from fastapi import APIRouter

from ..authentication import router as auth_router
from ..clients import router as clients_router
from ..configuration import router as configuraiton_router
from ..health_checks import router as health_checks_router
from ..users import router as users_rooter

router = APIRouter(prefix="/api")

router.include_router(health_checks_router, tags=["Health Checks"])
router.include_router(configuraiton_router, tags=["Configuration"])
router.include_router(clients_router, tags=["Clients"])
router.include_router(users_rooter, tags=["Users"])
router.include_router(auth_router, tags=["Users"])
