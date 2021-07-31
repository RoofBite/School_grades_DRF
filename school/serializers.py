from rest_framework import serializers
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User, PrincipalTeacher
from rest_framework.fields import CurrentUserDefault


class PrincipalTeacherSerializer:
    class Meta:
        model = PrincipalTeacher
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    principal = serializers.CharField(source='principalteacher')
    id = serializers.IntegerField()
    class Meta:
        model = School
        fields = '__all__'
        
        extra_kwargs = {'name': {'required': False}}

class SchoolSerializerForStudentList(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = School
        fields = ('id', 'name')
        
        extra_kwargs = {'name': {'required': False}}

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = School
        fields = '__all__'
        
class TeacherSerializerForClassList(serializers.ModelSerializer):
    
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', )

class TeacherSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(many=True)
    class Meta:
        model = Teacher
        fields = '__all__'

class TeacherSerializerForTeachersList(serializers.ModelSerializer):
    supervising_teacher = serializers.CharField(source='schoolclass')
    class Meta:
        model = Teacher
        fields = '__all__'




class SchoolSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = '__all__'
        extra_kwargs = {'name': {'required': False}}


class SchoolSubjectSerializerForClassList(serializers.ModelSerializer):
    teacher = TeacherSerializerForClassList("schoolclass", read_only=True, many=True)
    
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
        fields = ('id', 'name', 'supervising_teacher', 'school', 'subject')

class SchoolClassSerializerForList(serializers.ModelSerializer):
    id = serializers.IntegerField()
    supervising_teacher = TeacherSerializerForClassList(many=False)
    
    subject = SchoolSubjectSerializerForClassList(many=True)
    class Meta:
        model = SchoolClass
        fields = ('id', 'name', 'supervising_teacher', 'subject')

class SchoolClassSerializerForStudentList(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = SchoolClass
        fields = ('id', 'name')
        extra_kwargs = {'name': {'required': False}}



class StudentSerializer(serializers.ModelSerializer):
    current_user = serializers.HiddenField(
                                           default = serializers.CurrentUserDefault()
    )
    school_class = SchoolClassSerializerForStudentList(many=False, required=False)
    school = SchoolSerializerForStudentList(many=False, required=False)
    subject = SchoolSubjectSerializer(many=True, required=False)
    
    class Meta:
        model = Student
        fields = ('current_user', 'first_name', 'last_name', 'user', 'school_class', 'school', 'subject')
        extra_kwargs = {'user': {'required': False},'school_class': {'required': False},'school': {'required': False},'subject': {'required': False}}

    def create(self, data):
        if self.context['request'].user.is_staff:
            school_field = School.objects.get(id=data['school'].get('id'))
        else: 
            school_field = PrincipalTeacher.objects.filter(user__id=self.context['request'].user.id).first().school
        
        return Student.objects.create(user=User.objects.get(pk=data['user'].pk), first_name=data['first_name'], last_name=data['last_name'], school=school_field,
        school_class=SchoolClass.objects.get(pk=data['school_class'].get('id')))
    
    