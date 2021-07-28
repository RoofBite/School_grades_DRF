from django.contrib import admin
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, PrincipalTeacher


admin.site.register(School)
admin.site.register(SchoolClass)
admin.site.register(SchoolSubject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(PrincipalTeacher)

