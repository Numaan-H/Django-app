from django.contrib import admin

# Register your models here.
from .models import Issue, Course, Module

admin.site.register(Issue)
admin.site.register(Course)
admin.site.register(Module)