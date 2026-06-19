from django.contrib import admin

from .models import LineUser
from .models import LineLog


admin.site.register(LineUser)
admin.site.register(LineLog)