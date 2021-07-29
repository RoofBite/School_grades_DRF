from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length = 100,  null = True, blank = True)

    def __str__(self):
        return self.name

class PrincipalTeacher(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user = OneToOneField(User, on_delete = models.CASCADE)
    school = OneToOneField('School', on_delete = models.CASCADE)

    def __str__(self):
        return self.first_name + self.last_name

class Teacher(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user = OneToOneField(User, on_delete = models.CASCADE)
    school = models.ManyToManyField('School')

    def __str__(self):
        return self.first_name + self.last_name

class SchoolSubject(models.Model):
    name = models.CharField(max_length = 50, blank = True, null = True)
    teacher = models.ManyToManyField('Teacher')
    school = models.ForeignKey('School', on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.name

class SchoolClass(models.Model):
    name = models.CharField(max_length = 50)
    supervising_teacher = models.OneToOneField('Teacher', null=True, on_delete = models.CASCADE)
    school = models.ForeignKey('School', on_delete = models.CASCADE, null=True)
    subject = models.ManyToManyField('SchoolSubject')

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user = OneToOneField(User, on_delete = models.CASCADE, blank = True ,null = True)
    school_class = models.ForeignKey('SchoolClass', on_delete = models.SET_NULL, blank = True, null = True)
    school = models.ForeignKey('School', on_delete = models.SET_NULL, blank = True, null = True)
    subject = models.ManyToManyField('SchoolSubject', blank = True, null = True)

    def __str__(self):
        return self.first_name + self.last_name












