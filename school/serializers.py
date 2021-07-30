from rest_framework import serializers
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User

class SchoolSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = School
        fields = '__all__'
        extra_kwargs = {'name': {'required': False}}

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = School
        fields = '__all__'
        

class TeacherSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(many=True)
    class Meta:
        model = Teacher
        fields = '__all__'


class SchoolSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = '__all__'
        extra_kwargs = {'name': {'required': False}}

class SchoolClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    supervising_teacher = TeacherSerializer(many=False)
    school = SchoolSerializer(many=False)
    subject = SchoolSubjectSerializer(many=True)
    class Meta:
        model = SchoolClass
        fields = ('id', 'name')

class SchoolClassSerializerForStudentList(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SchoolClass
        fields = ('id', 'name')


class StudentSerializer(serializers.ModelSerializer):
    school_class = SchoolClassSerializerForStudentList(many=False, required=False)
    school = SchoolSerializer(many=False, required=False)
    subject = SchoolSubjectSerializer(many=True, required=False)
    
    class Meta:
        model = Student
        fields = ( 'first_name', 'last_name', 'user', 'school_class', 'school', 'subject')
        extra_kwargs = {'user': {'required': False},'school_class': {'required': False},'school': {'required': False},'subject': {'required': False}}

    def create(self, data):
        
        return Student.objects.create(user=User.objects.get(pk=data['user'].pk), first_name=data['first_name'], last_name=data['last_name'], school=School.objects.get(id=data['school'].get('id')),
        school_class=SchoolClass.objects.get(pk=data['school_class'].get('pk')))

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['school'] = SchoolSerializer(instance.school).data
        return response