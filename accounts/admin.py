from django.contrib import admin
from .models import User, Appeal

# Register your models here.

# admin.site.register(User)
admin.site.register(Appeal)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "is_suspended", "center", "polling_station")
