from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    shop = models.ForeignKey('main.Shop', on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    personal = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 101)])  
    purity = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 101)])  
    sorting = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 101)]) 
    created_at = models.DateTimeField(auto_now_add=True)


    def get_average_score(self):
        return (self.personal + self.purity + self.sorting) / 3