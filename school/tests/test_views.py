from rest_framework.test import APITestCase
from school.models import School, SchoolClass, SchoolSubject, Student, Teacher, User, Grade, Post
from school.api_views import ListSchoolTeachers
from rest_framework.test import APIClient
from django.urls import reverse

class TestListSchool(APITestCase):
    url = '/api/schools/'

    def setUp(self):
        School.objects.create(name='School1')
    
    def test_schools_GET(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['name'], 'School1')


class TestListSchoolTeachers(APITestCase):
    pk_url = '1'
    url = f'/api/schools/{pk_url}/teachers/'
    

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('username6', 'Pas$w0rd')
        self.client.force_authenticate(self.user)
    
    def test_teachers_list_GET(self):
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create( first_name="John",
last_name="Smith",user=self.user)
        teacher.school.add(school)

        response = self.client.get(reverse('school-teachers', kwargs={'pk': 1}))
        result = response.json()
        self.assertEqual(reverse('school-teachers', kwargs={'pk': 1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['first_name'], 'John')
        self.assertEqual(result[0]['last_name'], 'Smith')
        self.assertEqual(result[0]['user'], self.user.id)
        