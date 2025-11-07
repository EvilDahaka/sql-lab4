import logging
from fastapi import FastAPI

# from auth.router import router
from src.utils import load_routers

log = logging.getLogger(__name__)

app = FastAPI()
load_routers(app)


@app.get("/")
async def root():
    return {"ok": True}
