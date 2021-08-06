from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework import generics
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework import permissions
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User, Grade, Post
from .serializers import GradeSerializer, GradeSerializerPOST, SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializerForList, TeacherSerializer, TeacherSerializerForTeachersList, \
                         SchoolClassSerializerForList, StudentSerializerGrades, \
                         StudentsInSubjectSerializerForList, PostSerializer

from .permissions import TeacherPermission, PrincipalPermission, SubjectTeacherPermission, \
                         SubjectTeacherGradePermission, StudentGradePermission, \
                         SchoolPostsTeacherOrPrincipalPermission, SchoolPostDetailAuthor

        
#Pagination
class PostsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
def get_routes(request):

    routes = [
    {'POST, OPTIONS' : 'users/token/'},
    {'POST, OPTIONS' : 'users/token/refresh/'},
    {'GET, HEAD, OPTIONS' : '/api/schools'},
    {'GET, HEAD, OPTIONS' : '/api/schools/pk'},
    {'GET, HEAD, OPTIONS' : '/api/schools/pk/teachers'},
    {'GET, POST, HEAD, OPTIONS' : '/api/schools/pk/students'},
    {'GET, HEAD, OPTIONS' : '/api/schools/pk/classes'},
    {'GET, HEAD, OPTIONS' : '/api/subjects/<int:pk1>/students'},
    {'GET, PUT, PATCH, HEAD, OPTIONS' : '/api/subjects/<int:pk1>/students/<int:pk2>/'},
    {'GET, PUT, POST, HEAD, OPTIONS':'api/subjects/<int:pk1>/students/<int:pk2>/grades/<int:pk3>/'}
    ]

    return Response(routes)


class ListSchool(generics.ListAPIView):
    queryset = School.objects.all().select_related('principalteacher')
    serializer_class = SchoolSerializer

class DetailSchool(generics.RetrieveAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all().select_related('principalteacher')

class SchoolPostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    
    @property
    def permission_classes(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [SchoolPostDetailAuthor]
        elif self.request.method in ['GET']:
            return [SchoolPostDetailAuthor]
        return [IsAdminUser]

    def error404(request):
        raise NotFound(detail="Error 404, object not found", code=404)

    def get_object(self):
        pk1 =self.kwargs['pk1']
        pk2 =self.kwargs['pk2']

        try:
            obj = Post.objects.select_related('author','school').get(school__id=pk1, id=pk2)
            self.check_object_permissions(self.request, obj)
            return obj
        except Post.DoesNotExist:
            return self.error404()

class SchoolPosts(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    search_fields = ['title', 'body','author__last_name']
    filter_backends = (filters.SearchFilter,)
    
    @property
    def permission_classes(self):
        if self.request.method in ['POST']:
            return [SchoolPostsTeacherOrPrincipalPermission]
        elif self.request.method in ['GET']:
            return [AllowAny]
        return [IsAdminUser]


    def get_queryset(self):
        pk =self.kwargs['pk']
        
        return Post.objects.filter(school__id=pk).select_related('author', 'school')
        

class ListSchoolTeachers(generics.ListAPIView):
    serializer_class = TeacherSerializerForTeachersList
    
    def get_queryset(self):
        pk = self.kwargs['pk']

        return Teacher.objects.filter(school__id = pk).prefetch_related('school').select_related('user','schoolclass')

class ListSchoolStudents(generics.ListCreateAPIView):
    serializer_class = StudentSerializerForList

    @property
    def permission_classes(self):
        if self.request.method in ['POST']:
            return [PrincipalPermission]
        elif self.request.method in ['GET']:
            return [IsAuthenticated, TeacherPermission | PrincipalPermission]
        return [IsAdminUser]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(school__id = pk).select_related('school','school_class').prefetch_related('subject')

class ListSubjectStudents(generics.ListAPIView):
    serializer_class = StudentsInSubjectSerializerForList
    permission_classes = [SubjectTeacherPermission]
    lookup_field = 'pk'
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Student.objects.filter(subject__id=pk).select_related('school','school_class')

class StudentGradeInSubject(generics.ListCreateAPIView):
    lookup_field = ('pk1','pk2')
    serializer_class = GradeSerializerPOST

    @property
    def permission_classes(self):
        if self.request.method in ['POST']:
            return [SubjectTeacherGradePermission]
        elif self.request.method in ['GET']:
            return [SubjectTeacherGradePermission | StudentGradePermission]
        return [IsAdminUser]    
    
    def get_queryset(self):
        pk1 = self.kwargs['pk1']
        pk2 = self.kwargs['pk2']
        
        return Grade.objects.select_related('student', 'subject').filter(subject__id=pk1, student__user__id=pk2)

class StudentGradeInSubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = ('pk1','pk2','pk3')
    serializer_class = GradeSerializer
    
    @property
    def permission_classes(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [SubjectTeacherGradePermission]
        elif self.request.method in ['GET']:
            return [SubjectTeacherGradePermission | StudentGradePermission]
        return [IsAdminUser]    
    
    def get_object(self):
        pk1 = self.kwargs['pk1']
        pk2 = self.kwargs['pk2']
        pk3 = self.kwargs['pk3']
        
        return Grade.objects.select_related('student','subject').get(id=pk3, subject__id=pk1, student__user__id=pk2)

        

class StudentInSubjectDetail(generics.RetrieveAPIView):
    serializer_class = StudentSerializerGrades
    lookup_field = ('pk1','pk2')

    @property
    def permission_classes(self):
        if self.request.method in ['GET']:
            return [SubjectTeacherGradePermission | StudentGradePermission]
        return [IsAdminUser]

    def get_object(self):
        pk1 = self.kwargs['pk1']
        pk2 = self.kwargs['pk2']
        return Student.objects.select_related('school_class').get(subject__id=pk1, user__id=pk2)

class ListSchoolClasses(generics.ListAPIView):
    serializer_class = SchoolClassSerializerForList
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return SchoolClass.objects.filter(school__id=pk).select_related('supervising_teacher').prefetch_related('subject')
