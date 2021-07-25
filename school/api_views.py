from rest_framework import generics
from .models import School, SchoolClass, SchoolSubject, Student, Teacher
from .serializers import SchoolSerializer, SchoolClassSerializer, SchoolSubjectSerializer, \
                         StudentSerializer, TeacherSerializer

class ListSchool(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class DetailSchool(generics.RetrieveAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    