from django.contrib import admin

from .models import Applicants, Employees

# Register your models here.
admin.site.register(Employees)
admin.site.register(Applicants)
#admin.site.register(Employees)