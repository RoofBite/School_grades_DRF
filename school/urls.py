from django.urls import path, include
from .api_views import *

urlpatterns= [
    path('', get_routes),
    path('schools/', ListSchool.as_view()),
    path('schools/<int:pk>/', DetailSchool.as_view()),
    path('schools/<int:pk>/teachers/', ListSchoolTeachers.as_view()),
    path('schools/<int:pk>/students/', ListSchoolStudents.as_view()),
    path('schools/<int:pk>/classes/', ListSchoolClasses.as_view()),   
    
    
]