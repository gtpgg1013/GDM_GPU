from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
import os
import shutil
import zipfile
from pathlib import Path
# from tasks import _inference, add
# from worker.celery_app import celery_app
from threading import Thread
import logging
# from config.celery_utils import create_celery
from celery import current_app

log = logging.getLogger(__name__)

app = FastAPI()

class InferenceRequest(BaseModel):
    rds_id : int

def celery_on_message(body):
    log.warn(body)

def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# @app.post("/inference/{gen_model_id}")
# def gen_model_load(gen_model_id: int):
#     return {"gen_model_id": gen_model_id}

@app.get("/inference/{rds_id}")
async def inference(rds_id: int):
    task_name = "worker.celery_worker._inference"
    schedule = current_app.send_task(task_name, args=[rds_id])
    print(schedule.id)
    return {"schedule_id": schedule.id}