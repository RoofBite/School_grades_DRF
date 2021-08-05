from rest_framework import serializers
from .models import School, SchoolClass, SchoolSubject, Student, \
                    Teacher, User, PrincipalTeacher, Grade, Post
from rest_framework.fields import CurrentUserDefault



class PrincipalTeacherSerializer(serializers.ModelSerializer):
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

class UserSerializerForPostList(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = User
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializerForPostList(required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'author')
        extra_kwargs = {'author': {'required': False}}
        read_only_fields = ('author',)
    
    def create(self, validated_data):
        title = validated_data.pop('title')
        body = validated_data.pop('body')
        school_id = self.context['request'].resolver_match.kwargs.get('pk')
        school = School.objects.get(id=school_id)
        user = User.objects.get(id=self.context['request'].user.id)
        new_post = Post.objects.create(title=title, body=body, school=school, author=user )
        
        return new_post
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
        exclude = ('school', )


class SchoolSubjectSerializerForGrades(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = ('id','name')
        extra_kwargs = {'name': {'required': False}}

class SchoolSubjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SchoolSubject
        fields = '__all__'
        extra_kwargs = {'name': {'required': False},'id': {'required': False}}

class GradeSerializer(serializers.ModelSerializer):
    subject = SchoolSubjectSerializerForGrades(many=False, required=False)
    id = serializers.IntegerField(required=True)
    class Meta:
        model = Grade
        fields = ('id','value','subject')
        extra_kwargs = {'id': {'required': True}, 'subject': {'required': True}}

class GradeSerializerPOST(serializers.ModelSerializer):
    subject = SchoolSubjectSerializerForGrades(many=False, required=False)
    class Meta:
        model = Grade
        fields = ('id','value','subject')
        extra_kwargs = {'id': {'required': False}, 'subject': {'required': False}}

    def create(self, validated_data):
        # Independent of user input saves grade to subject and student which id's are pk1 and pk2
        value = validated_data.pop('value')
        subject_id = self.context['request'].resolver_match.kwargs.get('pk1')
        student_id = self.context['request'].resolver_match.kwargs.get('pk2')
        subject = SchoolSubject.objects.get(id=subject_id)
        student = Student.objects.get(user__id=student_id)
        grade = Grade.objects.create(value=value,subject=subject,student=student)

        return grade

class SchoolSubjectSerializerForClassList(serializers.ModelSerializer):
    teacher = TeacherSerializerForClassList("schoolclass", read_only=True, many=True)
    
    class Meta:
        model = SchoolSubject
        exclude = ('school',)
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

class StudentsInSubjectSerializerForList(serializers.ModelSerializer):
    school_class = SchoolClassSerializerForStudentList(many=False, required=False)
    
    class Meta:
        model = Student
        fields = ( 'first_name', 'last_name', 'user', 'school_class',)

class StudentSerializerGrades(serializers.ModelSerializer):
    current_user = serializers.HiddenField(
                                           default = serializers.CurrentUserDefault()
    )
    school_class = SchoolClassSerializerForStudentList(many=False, required=False)
    grades = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ('current_user', 'first_name', 'last_name', 'user', 'school_class', 'grades')
    
    def get_grades(self, obj):
        pk1 = self.context['request'].resolver_match.kwargs.get('pk1')
        pk2 = self.context['request'].resolver_match.kwargs.get('pk2')
        query = Grade.objects.filter(subject__id=pk1, student__user__id=pk2)
        return GradeSerializer(query, many=True).data

class StudentSerializerForList(serializers.ModelSerializer):
    current_user = serializers.HiddenField(
                                           default = serializers.CurrentUserDefault()
    )
    school_class = SchoolClassSerializerForStudentList(many=False, required=False)
    
    class Meta:
        model = Student
        fields = ('current_user', 'first_name', 'last_name', 'user', 'school_class', )
        extra_kwargs = {'user': {'required': False},'school_class': {'required': False},
                        'school': {'required': False},'subject': {'required': False}}

    def create(self, data):
        if self.context['request'].user.is_superuser:
            school_field = School.objects.get(id=data['school'].get('id'))
        else: 
            school_field = PrincipalTeacher.objects.filter(user__id=self.context['request'].user.id).first().school
        
        return Student.objects.create(user=User.objects.get(pk=data['user'].pk), first_name=data['first_name'],
                                      last_name=data['last_name'], school=school_field,
                                      school_class=SchoolClass.objects.get(pk=data['school_class'].get('id')))
    
    