from rest_framework import generics
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework import permissions
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializerForList, TeacherSerializer, TeacherSerializerForTeachersList, \
                         SchoolClassSerializerForList, StudentSerializerAddGrades, StudentsInSubjectSerializerForList
from .permissions import TeacherPermission, PrincipalPermission, SubjectTeacherPermission, \
                         SubjectTeacherAddGradesPermission

        


@api_view(['GET'])
def get_routes(request):

    routes = [
    {'POST, OPTIONS':'users/token/'},
    {'POST, OPTIONS':'users/token/refresh/'},
    {'GET, HEAD, OPTIONS': '/api/schools'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk/teachers'},
    {'GET, POST, HEAD, OPTIONS': '/api/schools/pk/students'},
    {'GET, HEAD, OPTIONS': '/api/schools/pk/classes'},
    {'GET, HEAD, OPTIONS': '/api/subjects/<int:pk1>/students'},
    {'GET, PUT, PATCH, HEAD, OPTIONS': '/api/subjects/<int:pk1>/students/<int:pk2>/'}
    
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

class ListSchoolStudents(generics.ListCreateAPIView):
    serializer_class = StudentSerializerForList

    @property
    def permission_classes(self):
        if self.request.method in ['POST']:
            return [PrincipalPermission ]
        elif self.request.method in ['GET']:
            return [IsAuthenticated, TeacherPermission | PrincipalPermission ]
        return [IsAdminUser]
    
    def get_queryset(self):
        self.check_object_permissions()
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk).select_related('school','school_class').prefetch_related('subject')

class ListSubjectStudents(generics.ListAPIView):
    serializer_class = StudentsInSubjectSerializerForList
    permission_classes = [SubjectTeacherPermission]
    lookup_field = 'pk'
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(subject__id=pk).select_related('school','school_class')

class StudentAddGrades(generics.RetrieveUpdateAPIView):
    serializer_class = StudentSerializerAddGrades
    permission_classes = [SubjectTeacherAddGradesPermission]
    lookup_field = ('pk1','pk2')

    def get_object(self):
        pk1 = self.kwargs['pk1']
        pk2 = self.kwargs['pk2']
        
        return Student.objects.get(subject__id=pk1, user__id=pk2)

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializerForList
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SchoolClass.objects.filter(school__id=pk).select_related('supervising_teacher').prefetch_related('subject')
