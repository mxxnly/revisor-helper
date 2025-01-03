from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=timezone.now)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    minutes_worked = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    bonus_added = models.BooleanField(default=False)

    def adjust_time(self):
        if self.minutes_worked >= 60:
            additional_hours = self.minutes_worked // 60
            self.hours_worked += additional_hours
            self.minutes_worked = self.minutes_worked % 60

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.hours_worked} годин, {self.minutes_worked} хвилин."
