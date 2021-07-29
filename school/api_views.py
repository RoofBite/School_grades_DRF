from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework import permissions
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializer, TeacherSerializer

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
                teacher_school_id = user.teacher.school.all().values_list('id', flat = True)
            else:
                teacher_school_id = False
        except:
            print("User is not teacher")

        if not obj.first():
            student_school_id = False
        else:
            student_school_id = obj.first().school.id

        if student_school_id == False or teacher_school_id == False:
            return False
        else:
            return student_school_id in teacher_school_id
        

        


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

class ListSchoolStudents(generics.ListCreateAPIView, TeacherPermission):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated & TeacherPermission]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk)

    def get_permissions(self):
        if self.request.method in ['POST']:
            
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated(), TeacherPermission(), permissions.IsAdminUser()]

    

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return SchoolClass.objects.filter(school__id = pk)
