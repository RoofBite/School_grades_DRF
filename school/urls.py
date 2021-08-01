from django.urls import path, include
from .api_views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns= [
    path('', get_routes),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schools/', ListSchool.as_view()),
    path('schools/<int:pk>/', DetailSchool.as_view()),
    path('schools/<int:pk>/teachers/', ListSchoolTeachers.as_view()),
    path('schools/<int:pk>/students/', ListSchoolStudents.as_view()),
    path('schools/<int:pk>/classes/', ListSchoolClasses.as_view()), 
    path('subjects/<int:pk1>/students/<int:pk2>/', StudentAddGrades.as_view()),
    
    
]