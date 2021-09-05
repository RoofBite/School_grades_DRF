from django.urls import path, include
from .api_views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("schools/", ListSchool.as_view()),
    path("schools/<int:pk>/", DetailSchool.as_view()),
    path("schools/<int:pk>/posts/", SchoolPosts.as_view(), name="school-posts"),
    path(
        "schools/<int:pk1>/posts/<int:pk2>/",
        SchoolPostDetail.as_view(),
        name="school-post-detail",
    ),
    path(
        "schools/<int:pk>/teachers/",
        ListSchoolTeachers.as_view(),
        name="school-teachers",
    ),
    path(
        "schools/<int:pk>/students/",
        ListSchoolStudents.as_view(),
        name="list-school-students",
    ),
    path(
        "schools/<int:pk>/classes/",
        ListSchoolClasses.as_view(),
        name="list-school-classes",
    ),
    path(
        "subjects/<int:pk>/students/",
        ListSubjectStudents.as_view(),
        name="list-subject-students",
    ),
    path(
        "subjects/<int:pk1>/students/<int:pk2>/",
        StudentInSubjectDetail.as_view(),
        name="student-detail",
    ),
    path(
        "subjects/<int:pk1>/students/<int:pk2>/grades/<int:pk3>/",
        StudentGradeInSubjectDetail.as_view(),
        name="student-grades",
    ),
    path(
        "subjects/<int:pk1>/students/<int:pk2>/grades/",
        StudentGradeInSubject.as_view(),
        name="student-grade-in-subject",
    ),
    
    
]
