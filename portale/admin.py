from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Notice, Lesson, OfficeHour, Student

admin.site.register(Notice)
admin.site.register(Lesson)
admin.site.register(OfficeHour)
admin.site.register(Student, UserAdmin)