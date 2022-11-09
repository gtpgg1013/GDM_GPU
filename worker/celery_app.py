import os

from celery import Celery

celery_app = Celery(
    "worker",
    broker="pyamqp://guest@localhost//"
)
celery_app.conf.task_routes = {
    "app.worker.celery_worker._inference": "inference-queue",
    "app.worker.celery_worker._train": "train-queue"
    }

celery_app.conf.update(task_track_started=True)