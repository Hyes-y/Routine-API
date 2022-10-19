from django.contrib import admin
from .models import Routine, RoutineDay, RoutineResult

admin.site.register(Routine)
admin.site.register(RoutineDay)
admin.site.register(RoutineResult)
