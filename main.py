from fastapi import FastAPI, HTTPException
import app
from fastapi.security import HTTPDigest

mumble_rest: FastAPI = FastAPI(
    title="Mumble server rest api",
    version="0.0.1",  # docs_url=None, redoc_url=None
)

mumble_rest.include_router(app.api.server_router.router, prefix="/server")


@mumble_rest.get("/")
async def root():
    return {"version": mumble_rest.version}
