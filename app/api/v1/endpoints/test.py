from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
async def test():
    """ Checking if server is alive or not"""
    return {"test": "test"}
