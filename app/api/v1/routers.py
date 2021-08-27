from fastapi import APIRouter
from .endpoints import league

router = APIRouter()
router.include_router(league.router, tags=["League"])