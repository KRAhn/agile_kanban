from django.contrib import admin
from kanban.models import Iteration

admin.site.register(Iteration, admin.ModelAdmin)