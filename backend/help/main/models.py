from django.db import models



# Create your models here.

class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    last_counted_by = models.ForeignKey('Revisor', on_delete=models.SET_NULL, null=True, blank=True, related_name='last_counted_shops')
    

    def __str__(self):
        return self.name

    
class Revisor(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_hired = models.DateField()
    now_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    shops = models.IntegerField()
    way_shops = models.IntegerField()
    move_shops = models.IntegerField()


    def __str__(self):
        return f"{self.firstname} {self.lastname}"

