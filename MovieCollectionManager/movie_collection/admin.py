from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from movie_collection.models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
