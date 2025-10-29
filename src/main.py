import logging
from fastapi import FastAPI

# from auth.router import router
from utils import load_routers

log = logging.getLogger(__name__)

app = FastAPI()
routers = load_routers()
if routers:
    app.include_router(routers)


@app.get("/")
async def root():
    return {"ok": True}
