from celery import Celery

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
    # result_backend=settings.REDIS_URL
)

celery_instance.conf.beat_schedule = {
    "luboe_nazvanie": {
        "task": "booking_today_check_in",
        "schedule": 5,
    }
}
