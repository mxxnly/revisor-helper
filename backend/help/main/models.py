from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from rate.models import Rating
from django.db.models import F


class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    last_counted_by = models.ForeignKey('Revisor', on_delete=models.SET_NULL, null=True, blank=True, related_name='last_counted_shops')
    position = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('transported', 'Transported'),('c1', 'C1'),('away', 'Away'),('normal', 'Normal')], default="normal")
    last_time = models.DateTimeField(null=True, blank=True)
    last_revision = models.FloatField(null=True, blank=True)
    avg_rating = models.FloatField(blank=True, null=True)
    avg_personal = models.FloatField(blank=True, null=True)
    avg_purity = models.FloatField(blank=True, null=True)
    avg_sorting = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['position']
    

    def __str__(self):
        return self.name
    
    
    
    def upd_avg_rating(self):
        ratings = self.ratings.all()
        total_ratings = ratings.count()
        if total_ratings > 0:
            avg = sum([rating.get_average_score() for rating in ratings]) / total_ratings
            self.avg_rating = round(avg, 2)
            self.save()
    
    def upd_avg_ratings(self):
        try:
            ratings = self.ratings.all()
            total_ratings = ratings.count()

            if total_ratings > 0:
                avg_personal = sum(rating.personal for rating in ratings) / total_ratings
                avg_purity = sum(rating.purity for rating in ratings) / total_ratings
                avg_sorting = sum(rating.sorting for rating in ratings) / total_ratings

                self.avg_personal = round(avg_personal, 2)
                self.avg_purity = round(avg_purity, 2)
                self.avg_sorting = round(avg_sorting, 2)
            else:
                self.avg_personal = None
                self.avg_purity = None
                self.avg_sorting = None

            self.save()
        except Exception as e:
            print(f"Error updating average ratings: {e}")
            
class Photo(models.Model):
    shop = models.ForeignKey(Shop, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')

class Video(models.Model):
    shop = models.ForeignKey(Shop, related_name='videos', on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')

    
class Revisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='revisor', null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_hired = models.DateField(default='2000-01-01')
    now_shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True)
    shops = models.IntegerField(default=0)
    way_shops = models.IntegerField(default=0)
    move_shops = models.IntegerField(default=0)
    plus_or_minus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    favourite_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='fav_shop', blank=True, null=True)
    date_of_birth = models.DateField(default='2000-01-01')
    who_are = models.CharField(max_length=20, choices=[('ревізор', 'Ревізор'),('стажер', 'Стажер')], default="Ревізор")

    def update_favourite_shop(self):
        highest_rated_shop = Rating.objects.filter(user=self.user).annotate(avg_score=(
            (F('personal') + F('purity') + F('sorting')) / 3
        )).order_by('-avg_score').first()
        
        if highest_rated_shop:
            self.favourite_shop = highest_rated_shop.shop
            self.save()
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
class Task(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    revisor = models.ForeignKey('Revisor', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    plus = models.IntegerField(default=0) 
    minus = models.IntegerField(default=0)

    def complete_task(self):
        self.completed_at = timezone.now()
        self.save()

        self.shop.last_time = self.completed_at
        self.shop.save()

@receiver(post_save, sender=User)
def assign_revisor(sender, instance, created, **kwargs):
    if created:
        try:
            revisor = Revisor.objects.get(email=instance.email)
            revisor.user = instance
            revisor.save()
        except Revisor.DoesNotExist:
            pass