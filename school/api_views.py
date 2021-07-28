from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework import permissions
from rest_framework.response import Response
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializer, TeacherSerializer

class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Checks if id of school on that route is in id's of schools to which the teacher is asigned 
        user = User.objects.filter(id = request.user.id).first()
        pk = request.resolver_match.kwargs.get('pk')
        obj=Student.objects.filter(school__id = pk)
        
        return obj.first().school.id in user.teacher.school.all().values_list('id', flat=True)
        

        


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

#Restricted to see only by teachers assigned to specific school

class ListSchoolStudents(generics.ListAPIView, TeacherPermission):
    serializer_class = StudentSerializer
    permission_classes = [TeacherPermission, IsAuthenticated]
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk)

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SchoolClass.objects.filter(school__id = pk)
