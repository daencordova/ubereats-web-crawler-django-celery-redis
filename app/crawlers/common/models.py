import uuid

from django.db import models


class CrawlerErrorLog(models.Model):

    error_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_name = models.CharField(max_length=256)
    task_args = models.JSONField(default=list, blank=True)
    task_kwargs = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)

    def __str__(self):
        return f"ubereats.error_log <Name Task:{self.task_name}>"

    class Meta:
        db_table = "ubereats_error_log"
        verbose_name_plural = "ErrorLog"
