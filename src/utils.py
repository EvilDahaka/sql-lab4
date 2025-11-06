# src/routes/__init__.py
import os
from fastapi import APIRouter
import importlib
from pathlib import Path
import logging

log = logging.getLogger("fastapi")


FILENAME = "router.py"  # можна доповнювати через конфіг


def load_routers():
    log.info("start load router")
    router = APIRouter()
    for file in os.listdir(Path(__file__).parent):
        package_path = Path(__file__).parent / file
        file_path = package_path / FILENAME
        # only consider directories that contain the router file
        if package_path.is_dir() and file_path.exists():
            # module name should be like '<package>.router' (e.g. 'modpack.router')
            module_name = f"src.{file}.router"
            try:
                module = importlib.import_module(module_name)
                router.include_router(module.router)
                log.info(f"router {file_path} loaded")
            except Exception as e:
                log.exception(f"failed to import router module {module_name}: {e}")

    return router
