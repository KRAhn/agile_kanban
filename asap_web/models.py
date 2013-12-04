from django.contrib.auth.models import User
from django.db import models


class AccessLog(models.Model):
    trace_key = models.CharField(max_length=64, db_index=True)
    path = models.CharField(max_length=255)
    query_string = models.CharField(max_length=255)
    ip = models.CharField(max_length=15)
    referer = models.TextField()
    log_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
