from django.contrib import admin
from .models import TypeAnswer, Theme, Task, TaskList, UserTheme, DoneTask

# Реєстрація моделей за замовчуванням
admin.site.register(TypeAnswer)
admin.site.register(Theme)


# Створення класів адміністратора для кастомізації відображення
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'point', 'theme', 'type_ans')  # вказуємо поля, які хочемо бачити в списку
    search_fields = ('name', 'theme__name')  # додаємо можливість пошуку за цими полями


admin.site.register(Task, TaskAdmin)


class TaskListAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_weekly')
    search_fields = ('user__username', 'task__name')


admin.site.register(TaskList, TaskListAdmin)


class UserThemeAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme')
    search_fields = ('user__username', 'theme__name')


admin.site.register(UserTheme, UserThemeAdmin)


class DoneTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_done', 'datetime')
    search_fields = ('user__username', 'task__name')
    list_filter = ('is_done',)  # додаємо фільтр за полем is_done


admin.site.register(DoneTask, DoneTaskAdmin)
