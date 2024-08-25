from django.db import models
from main.models import Revisor
from django.utils import timezone
from django.contrib.auth.models import User

class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=timezone.now)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)


    def __str__(self):
        return f"{self.revisor.firstname} {self.revisor.lastname} - {self.date} - {self.hours_worked} hours"