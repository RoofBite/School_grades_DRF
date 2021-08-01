from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework import permissions
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializer, TeacherSerializer, TeacherSerializerForTeachersList, SchoolClassSerializerForList

class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_staff:
            return True
        # Checks if id of school on that route is in id's of schools to which the teacher is asigned 
        user = User.objects.filter(id = request.user.id).first()
        pk = request.resolver_match.kwargs.get('pk')
        obj = Student.objects.filter(school__id = pk)
        teacher_school_id = False

        try:
            if user.teacher:
                # Obtains list of id's of schools to which teacher is assigned
                teacher_school_id = user.teacher.school.all().values_list('id', flat = True)
            else:
                teacher_school_id = False
        except:
            print("User is not teacher")

        # Attempts to take id of school to which student is assigned
        if not obj.first():
            student_school_id = False
        else:
            student_school_id = obj.first().school.id

        # Grants permission if student and teacher are asigned to the same school
        if student_school_id == False or teacher_school_id == False:
            return False
        else:
            return student_school_id in teacher_school_id
        
class PrincipalPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_staff:
            return True

        # Checks if id of school on that route is in id's of schools to which the principal is asigned 
        user = User.objects.filter(id = request.user.id).first()
        pk = request.resolver_match.kwargs.get('pk')
        obj = Student.objects.filter(school__id = pk)
        principal_school_id = False

        try:
            if user.principalteacher:
                principal_school_id = user.principalteacher.school.id
            else:
                principal_school_id = False
        except:
            print("User is not principal")

        if not obj.first():
            student_school_id = False
        else:
            student_school_id = obj.first().school.id

        if student_school_id == False or principal_school_id == False:
            return False
        else:
            return student_school_id == principal_school_id
        
        


@api_view(['GET'])
def get_routes(request):

    routes = [
    {'GET, HEAD, OPTIONS': '/api/schools'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk/teachers'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk/students'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk/classes'},

    ]

    return Response(routes)


class ListSchool(generics.ListAPIView):
    queryset = School.objects.all().select_related('principalteacher')
    serializer_class = SchoolSerializer

class DetailSchool(generics.RetrieveAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all().select_related('principalteacher')


class ListSchoolTeachers(generics.ListAPIView):
    serializer_class = TeacherSerializerForTeachersList
    
    def get_queryset(self):
        pk = self.kwargs['pk']

        return Teacher.objects.filter(school__id = pk).prefetch_related('school').select_related('user','schoolclass')

#Restricted to see only by Admin, teachers assigned to specific school and pricipal of school

class ListSchoolStudents(generics.ListCreateAPIView, TeacherPermission):
    serializer_class = StudentSerializer
    #permission_classes = [IsAuthenticated & TeacherPermission]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk).select_related('school','school_class').prefetch_related('subject')

    def get_permissions(self):
        if self.request.method in ['POST']:
            
            return [PrincipalPermission()]
        return [AllowAny()]
        #return [permissions.IsAuthenticated(), TeacherPermission()]

    

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializerForList
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SchoolClass.objects.filter(school__id = pk).select_related('supervising_teacher').prefetch_related('subject')
