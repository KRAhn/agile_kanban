from django.contrib import admin
from kanban.models import Iteration, Task

admin.site.register(Iteration, admin.ModelAdmin)
admin.site.register(Task, admin.ModelAdmin)