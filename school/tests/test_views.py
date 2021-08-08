from rest_framework.test import APITestCase
from school.models import School, SchoolClass, SchoolSubject, Student, Teacher, User, Grade, Post, PrincipalTeacher
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

    def test_post_detail_DELETE(self):
        school = School.objects.create(name='School1')
        Post.objects.create(title='Post1', body='Body1', author=self.user, school=school) 
        
        response = self.client.delete(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}))
        
        self.assertEqual(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), self.url)
        self.assertEqual(response.status_code, 204)

    def test_post_detail_POST(self):
        school = School.objects.create(name='School1')
        Post.objects.create(title='Post1', body='Body1', author=self.user, school=school) 
        data = {"title": "Post2", "body": "Body2"}
        
        response = self.client.post(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), data=data)
        result = response.json()

        self.assertEqual(reverse('school-post-detail', kwargs={'pk1':1,'pk2':1}), self.url)
        self.assertEqual(response.status_code, 403)
 
class TestSchoolPosts(APITestCase):
    pk_url = '1'
    url = f'/api/schools/{pk_url}/posts/'
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(self.user)

    def test_post_list_GET(self):
        school = School.objects.create(name='School1')
        Post.objects.create(title='Post1', body='Body1', author=self.user, school=school) 
        response = self.client.get(reverse('school-posts', kwargs={'pk':1}))
        result = response.json()

        self.assertEqual(reverse('school-posts', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result['results'], list)
        self.assertEqual(result['results'][0]['title'], 'Post1')
        self.assertEqual(result['results'][0]['body'], 'Body1')

    def test_post_list_POST(self):
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user)
        teacher.school.add(school)

        data = {"title": "Post1", "body": "Body1"}
        response = self.client.post(reverse('school-posts', kwargs={'pk':1}), data=data)
        result = response.json()

        self.assertEqual(reverse('school-posts', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['title'], 'Post1')
        self.assertEqual(result['body'], 'Body1')
    
    def test_post_list_PUT(self):
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user)
        teacher.school.add(school)

        data = {"title": "Post1", "body": "Body1"}
        response = self.client.put(reverse('school-posts', kwargs={'pk':1}), data=data)
        result = response.json()

        self.assertEqual(reverse('school-posts', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 403)

class TestListSchoolStudents(APITestCase):
    pk_url = '1'
    url = f'/api/schools/{pk_url}/students/'
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user('username1', 'Pas$w0rd')
        self.user2 = User.objects.create_user('username2', 'Pas$w0rd')
        self.user3 = User.objects.create_user('username3', 'Pas$w0rd')
        self.client.force_authenticate(self.user1)
        
    def test_students_list_GET(self):
        school = School.objects.create(name='School1')
        PrincipalTeacher.objects.create(first_name='Principal', last_name='PrincipalLast',
                                        user=self.user1, school=school) 
        Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=school)

        response = self.client.get(reverse('list-school-students', kwargs={'pk':1}))
        result = response.json()

        self.assertEqual(reverse('list-school-students', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['first_name'], 'Student')
        self.assertEqual(result[0]['last_name'], 'StudentLast')

    def test_students_list_POST(self):
        school = School.objects.create(name='School1')
        principal = PrincipalTeacher.objects.create(first_name='Principal', last_name='PrincipalLast',
                                        user=self.user1, school=school)
        
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user2)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        school_class = SchoolClass.objects.create(name='1', supervising_teacher=teacher, school=school)
        school_class.subject.add(subject)

        data = {
        "first_name": "Student",
        "last_name": "StudentLast",
        "user": 3,
        "school_class": {
            "id": 1
        }}

        response = self.client.post(reverse('list-school-students', kwargs={'pk':1}), data=data, format='json')
        result = response.json()

        self.assertEqual(reverse('list-school-students', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], 'Student')
        self.assertEqual(result['last_name'], 'StudentLast')
    
    def test_students_list_PUT(self):
        school = School.objects.create(name='School1')
        principal = PrincipalTeacher.objects.create(first_name='Principal', last_name='PrincipalLast',
                                        user=self.user1, school=school)
        
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user2)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        school_class = SchoolClass.objects.create(name='1', supervising_teacher=teacher, school=school)
        school_class.subject.add(subject)

        data = {
        "first_name": "Student",
        "last_name": "StudentLast",
        "user": 3,
        "school_class": {
            "id": 1
        }}

        response = self.client.put(reverse('list-school-students', kwargs={'pk':1}), data=data, format='json')
        result = response.json()

        self.assertEqual(reverse('list-school-students', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 403)

# Teacher.objects.filter(user__id=request.user.id, schoolsubject__id=pk).exists():
class TestListSubjectStudents(APITestCase):
    pk_url = '1'
    url = f'/api/subjects/{pk_url}/students/'
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user('username1', 'Pas$w0rd')
        self.user2 = User.objects.create_user('username2', 'Pas$w0rd')
        self.client.force_authenticate(self.user1)

    def test_subject_students_list_GET(self):
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user1)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        student = Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=school)
        student.subject.add(subject)
        
        response = self.client.get(reverse('list-subject-students', kwargs={'pk':1}))
        result = response.json()

        self.assertEqual(reverse('list-subject-students', kwargs={'pk':1}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['first_name'], 'Student')
        self.assertEqual(result[0]['last_name'], 'StudentLast')

class TestStudentGradeInSubject(APITestCase):
    pk_url1 = '1'
    pk_url2 = '2'
    url = f'/api/subjects/{pk_url1}/students/{pk_url2}/grades/'
    
    #Teacher.objects.filter(user__id=request.user.id, schoolsubject__id=pk).exists():
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user('username1', 'Pas$w0rd')
        self.user2 = User.objects.create_user('username2', 'Pas$w0rd')
        
    def test_student_grade_in_subject_student_GET(self):
        self.client.force_authenticate(self.user2)
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user1)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        student = Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=school)
        student.subject.add(subject)
        Grade.objects.create(value=1,subject=subject,student=student)

        response = self.client.get(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}))
        result = response.json()

        self.assertEqual(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['value'], 1)
        self.assertEqual(result[0]['subject']['id'], 1)
        self.assertEqual(result[0]['subject']['name'], 'subject')
    
    def test_student_grade_in_subject_teacher_GET(self):
        self.client.force_authenticate(self.user1)
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user1)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        student = Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=school)
        student.subject.add(subject)
        Grade.objects.create(value=1,subject=subject,student=student)
        
        response = self.client.get(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}))
        result = response.json()

        self.assertEqual(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}), self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['value'], 1)
        self.assertEqual(result[0]['subject']['id'], 1)
        self.assertEqual(result[0]['subject']['name'], 'subject')
    
    def test_student_grade_in_subject_teacher_PUT(self):
        self.client.force_authenticate(self.user1)
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user1)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        student = Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=school)
        student.subject.add(subject)
        Grade.objects.create(value=1,subject=subject,student=student)
        
        response = self.client.put(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}))

        self.assertEqual(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}), self.url)
        self.assertEqual(response.status_code, 403)
    
    def test_student_grade_in_subject_teacher_POST(self):
        self.client.force_authenticate(self.user1)
        school = School.objects.create(name='School1')
        teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user1)
        teacher.school.add(school)
        subject = SchoolSubject.objects.create(name='subject', teacher=teacher, school=school)
        student = Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=school)
        student.subject.add(subject)
        #Grade.objects.create(value=1,subject=subject,student=student)
        data = {"value": 2}
        response = self.client.post(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}),  data=data, format='json')
        result = response.json()

        self.assertEqual(reverse('student-grade-in-subject', kwargs={'pk1':1,'pk2':2}), self.url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['value'], 2)
        self.assertEqual(result['subject']['id'], 1)
        self.assertEqual(result['subject']['name'], 'subject')