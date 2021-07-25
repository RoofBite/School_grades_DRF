from django.urls import path, include
from .api_views import *

urlpatterns= [
    path('schools/',ListSchool.as_view())
]