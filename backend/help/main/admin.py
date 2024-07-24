from django.contrib import admin
from django.contrib.auth.models import Group,User

from .models import Revisor, Shop
# Register your models here.


admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "password"]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)

admin.site.register(Revisor)
admin.site.register(Shop)