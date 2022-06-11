from django.utils import autoreload


def run_celery():
    from appserver import celery_app

    celery_app.worker_main(
        [
            "-Aappserver",
            "worker",
            "-linfo",
            "-Ofair",
            "--prefetch-multiplier=4",
            "--autoscale=4,2",
            "--logfile=logs/celery.log",
        ]
    )


print("Starting celery worker with autoreload...")
autoreload.run_with_reloader(run_celery)
