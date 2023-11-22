from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'score', 'count_tasks')
    # You can add more customization here


admin.site.register(User, UserAdmin)
