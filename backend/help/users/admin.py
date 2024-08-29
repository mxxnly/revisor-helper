from django.contrib import admin
from django.contrib.auth.models import Group,User

from main.models import Revisor, Shop, Task



class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "password", "email", "groups" ]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)

admin.site.register(Revisor)
admin.site.register(Shop)
admin.site.register(Task)