import os
from celery import Celery
from dotenv import load_dotenv
from .generate_task import register_tasks

load_dotenv()

def make_celery(app_name, broker_url, backend_url):
    """
    Initialize and return a Celery instance.
    """
    celery = Celery(
        app_name,
        broker=broker_url,
        backend=backend_url,
    )
    return celery

def configure_celery(app):
    """
    Configures Celery with the provided Flask app.

    Args:
        app: The Flask app instance to integrate with Celery.
    """
    app.config.update(
        CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL"),
        CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND")
    )
    celery = make_celery(
        app.import_name,
        app.config["CELERY_BROKER_URL"],
        app.config["CELERY_RESULT_BACKEND"]
    )
    register_tasks(celery)
    return celery