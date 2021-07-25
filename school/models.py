from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User



class Student(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user = OneToOneField(User, on_delete = models.CASCADE)

class Teacher(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user = OneToOneField(User, on_delete = models.CASCADE)

class SchoolSubject(models.Model):
    name = models.CharField(max_length = 50)
    teacher = models.ManyToManyField(Teacher)
    student = models.ForeignKey(Student, on_delete = models.SET_NULL, null=True)

class SchoolClass(models.Model):
    name = models.CharField(max_length = 50)
    supervising_teacher = models.ManyToManyField(Teacher)
    member = models.ForeignKey(Student, on_delete = models.SET_NULL, null=True)
    subject = models.ManyToManyField(SchoolSubject)

class School(models.Model):
    name = models.CharField(max_length = 100)
    teacher = models.ManyToManyField(Teacher)
    student = models.ForeignKey(Student, on_delete = models.SET_NULL, null=True)
    school_class = models.ForeignKey(SchoolClass, on_delete = models.CASCADE)

