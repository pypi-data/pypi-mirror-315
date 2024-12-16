from fastapi import APIRouter
from sorting_api.routing.endpoints.sort import sort_router
from sorting_api.routing.endpoints.random import random_router

router = APIRouter()

router.include_router(sort_router)
router.include_router(random_router)