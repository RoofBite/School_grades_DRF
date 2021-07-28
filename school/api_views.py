from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import School, SchoolClass, SchoolSubject, Student, Teacher
from .permissions import TeacherPermission
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializer, TeacherSerializer


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
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class DetailSchool(generics.RetrieveAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

class ListSchoolTeachers(generics.ListAPIView):
    serializer_class = TeacherSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']

        return Teacher.objects.filter(school__id = pk).prefetch_related('school')

#Maybe later will be restricted to see only by teachers 
@permission_classes([IsAuthenticated])
class ListSchoolStudents(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = (TeacherPermission,)
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk)

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SchoolClass.objects.filter(school__id = pk)
