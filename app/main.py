from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import router
from mangum import Mangum


app = FastAPI(title='lol-insight-api')
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://daiv.netlify.app/",
    "https://daiv.app/",
    "https://www.daiv.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/v1")


@app.get("/",  tags=["Endpoint Test"])
def test():
    return {"message": "Welcome CI/CD Pipeline with GitHub Actions!"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)