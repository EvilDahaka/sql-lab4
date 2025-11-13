import logging
from fastapi import FastAPI

# from auth.router import router
from src.utils import load_routers
from src.load_models import load_all_orm_models


log = logging.getLogger(__name__)

load_all_orm_models()

app = FastAPI()
load_routers(app)


@app.get("/")
async def root():
    return {"ok": True}
