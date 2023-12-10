from django.contrib import admin
from .models import TypeAnswer, Theme, Task, TaskList, UserTheme


@admin.register(TypeAnswer)
class TypeAnswerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'point', 'theme', 'type_ans')
    list_filter = ('theme', 'type_ans')
    search_fields = ('name', 'text')


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_weekly')
    list_filter = ('is_weekly',)
    search_fields = ('user__username', 'task__name')


@admin.register(UserTheme)
class UserThemeAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme')
    search_fields = ('user__username', 'them__name')


