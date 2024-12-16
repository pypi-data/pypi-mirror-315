from fastapi import APIRouter
from app.routing.endpoints.sort import sort_router
from app.routing.endpoints.random import random_router

router = APIRouter()

router.include_router(sort_router)
router.include_router(random_router)