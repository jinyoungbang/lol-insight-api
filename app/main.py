from fastapi import FastAPI
from .api.v1.routers import router
from mangum import Mangum


app = FastAPI(title='lol-insight-api')
app.include_router(router, prefix="/v1")


@app.get("/",  tags=["Endpoint Test"])
def test():
    return {"message": "Welcome CI/CD Pipeline with GitHub Actions!"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)