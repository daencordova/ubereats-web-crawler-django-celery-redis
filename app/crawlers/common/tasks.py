from celery import shared_task

from .models import CrawlerErrorLog


@shared_task(name="start_log_error_task")
def start_log_error_task(request, exc, traceback):
    CrawlerErrorLog.objects.create(
        task_name=request.task,
        task_args=request.args,
        task_kwargs=request.kwargs,
        error=traceback,
    )
