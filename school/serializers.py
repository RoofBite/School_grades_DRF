from rest_framework import serializers
from .models import School, SchoolClass, SchoolSubject, Student, Teacher

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model=School
        fields= '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(many=True)
    class Meta:
        model=Teacher
        fields= '__all__'


class SchoolSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolSubject
        fields= '__all__'




class SchoolClassSerializer(serializers.ModelSerializer):
    supervising_teacher = TeacherSerializer(many=False)
    school = SchoolSerializer(many=False)
    subject = SchoolSubjectSerializer(many=True)
    class Meta:
        model=SchoolClass
        fields= '__all__'


class StudentSerializer(serializers.ModelSerializer):
    school_class = SchoolClassSerializer(many=False)
    school = SchoolSerializer(many=False)
    subject= SchoolSubjectSerializer(many=True)
    class Meta:
        model=Student
        fields= '__all__'
