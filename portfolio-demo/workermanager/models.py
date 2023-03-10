from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import datetime

class WorkingTimeModel(models.Model):
    worker = models.CharField(max_length=30)
    start = models.DateTimeField(default=timezone.now)
    finish = models.DateTimeField(default=timezone.now)
    
    work_time = datetime.timedelta(minutes=0)