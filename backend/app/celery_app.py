import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env if present
PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)

from celery import Celery
from celery.schedules import crontab
from app import create_app


def make_celery(app):
    redis_url = app.config.get("REDIS_URL")
    celery = Celery(
        app.import_name,
        backend=redis_url,
        broker=redis_url
    )
    celery.conf.update(app.config)

    # Schedule periodic tasks
    celery.conf.beat_schedule = {
        'cleanup-old-data-every-10-minutes': {
            'task': 'app.celery_app.cleanup_old_data',
            'schedule': crontab(minute='*/10'),  # every 10 minutes
        },
    }


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Create Flask app and Celery instance
backend_app = create_app(os.environ.get("CONFIG_NAME"))
celery = make_celery(backend_app)


# Example task
@celery.task
def send_email_task(to_email, subject, body):
    """Background task to send emails."""
    # Email sending logic here
    print(f"Sending email to {to_email}: {subject}")
    return f"Email sent to {to_email}"


@celery.task
def cleanup_old_data():
    """Periodic task to cleanup old data."""
    with backend_app.app_context():
        # Cleanup logic here
        print("Cleaning up old data...")
        return "Cleanup completed"
