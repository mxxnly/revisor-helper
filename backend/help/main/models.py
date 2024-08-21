from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    last_counted_by = models.ForeignKey('Revisor', on_delete=models.SET_NULL, null=True, blank=True, related_name='last_counted_shops')
    position = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('transported', 'Transported'),('c1', 'C1'),('away', 'Away'),('normal', 'Normal')], default="normal")
    last_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['position']


    def __str__(self):
        return self.name

    
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


    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
class Task(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    revisor = models.ForeignKey('Revisor', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

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