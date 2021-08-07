from rest_framework.test import APITestCase
from school.models import School, SchoolClass, SchoolSubject, Student, Teacher, User, Grade, Post
from school.api_views import ListSchoolTeachers
from rest_framework.test import APIClient
import json

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
        self.user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(self.user)
    
    def test_teachers_list_GET(self):
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user)
        teacher.school.add(school)

        response = self.client.get(reverse('school-teachers', kwargs={'pk': 1}))
        result = response.json()
        self.assertEqual(reverse('school-teachers', kwargs={'pk': 1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['first_name'], 'John')
        self.assertEqual(result[0]['last_name'], 'Smith')
        self.assertEqual(result[0]['user'], self.user.id)


class TestSchoolPostDetail(APITestCase):
    pk_url1 = '1'
    pk_url2 = '1'
    url = f'/api/schools/{pk_url1}/posts/{pk_url2}/'
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(self.user)

    def test_post_detail_GET(self):
        school = School.objects.create(name='School1')
        Post.objects.create(title='Post1', body='Body1', author=self.user, school=school) 
        response = self.client.get(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}))
        result = response.json()
    
        self.assertEqual(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['title'], 'Post1')
        self.assertEqual(result['body'], 'Body1')
    
    def test_post_detail_GET_404(self):
        school = School.objects.create(name='School1')
        response = self.client.get(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}))
        result = response.json()
        
        self.assertEqual(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), self.url)
        self.assertEqual(response.status_code, 404)
    
    def test_post_detail_PUT(self):
        school = School.objects.create(name='School1')
        Post.objects.create(title='Post1', body='Body1', author=self.user, school=school) 
        data = {"title": "Post2", "body": "Body2"}
        
        response = self.client.put(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), data=data)
        result = response.json()

        self.assertEqual(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['title'], 'Post2')
    
    def test_post_detail_PATCH(self):
        school = School.objects.create(name='School1')
        Post.objects.create(title='Post1', body='Body1', author=self.user, school=school) 
        data = {"title": "Post2", "body": "Body2"}
        
        response = self.client.patch(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), data=data)
        result = response.json()
        
        self.assertEqual(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['title'], 'Post2')
        
