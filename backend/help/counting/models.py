from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=timezone.now)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    bonus_minutes = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.hours_worked} hours"
