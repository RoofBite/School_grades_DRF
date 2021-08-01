from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework import permissions
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializerForList, TeacherSerializer, TeacherSerializerForTeachersList, SchoolClassSerializerForList
from .permissions import TeacherPermission, PrincipalPermission
   
        


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
    serializer_class = StudentSerializerForList
    permission_classes = [IsAuthenticated & TeacherPermission]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk).select_related('school','school_class').prefetch_related('subject')

    def get_permissions(self):
        if self.request.method in ['POST']:
            
            return [PrincipalPermission()]
        #return [AllowAny()]
        return [permissions.IsAuthenticated(), TeacherPermission()]

#class StudentDetail(generics.ListCreateAPIView, TeacherPermission):

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializerForList
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SchoolClass.objects.filter(school__id = pk).select_related('supervising_teacher').prefetch_related('subject')
