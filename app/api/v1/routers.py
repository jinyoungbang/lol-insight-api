from fastapi import APIRouter
from .endpoints import league, test

router = APIRouter()
router.include_router(league.router, tags=["League"])
router.include_router(test.router, tags=["Test"])