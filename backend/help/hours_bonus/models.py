from django.db import models
from django.contrib.auth.models import User
 
class bonus_hours(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True,blank=True,default=2024)
    hours = models.FloatField(null=True, blank=True, default=0)
    minutes = models.IntegerField(null=True, blank=True, default=0)
    
    class Meta:
        unique_together = ('user', 'month', 'year')
        
        
    def __str__(self):
        return f"{self.user}'s month {self.month}"
    
