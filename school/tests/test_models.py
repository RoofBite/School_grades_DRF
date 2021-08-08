from django.test import TestCase
from school.models import School, SchoolClass, SchoolSubject, \
                          Student, Teacher, User, Grade, Post, PrincipalTeacher
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

class TestModels(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user('username1', 'Pas$w0rd')
        self.user2 = User.objects.create_user('username2', 'Pas$w0rd')
        self.user3 = User.objects.create_user('username3', 'Pas$w0rd')
        self.user4 = User.objects.create_user('First', 'Pas$w0rd') 
        self.client.force_authenticate(self.user4)
        
        self.school = School.objects.create(name='School1')
        self.principal = PrincipalTeacher.objects.create(first_name='Principal', last_name='PrincipalLast',
                                        user=self.user1, school=self.school)
        self.teacher = Teacher.objects.create(first_name="John", last_name="Smith", user=self.user2)
        self.teacher.school.add(self.school)
        self.subject = SchoolSubject.objects.create(name='subject', teacher=self.teacher, school=self.school)
        self.school_class = SchoolClass.objects.create(name='1', supervising_teacher=self.teacher, school=self.school)
        self.school_class.subject.add(self.subject)
        self.student = Student.objects.create(user=self.user2, first_name='Student',
                               last_name='StudentLast', school=self.school)
        self.student.subject.add(self.subject)
        self.post = Post.objects.create(title='Post1', body='Body1', author=self.user4, school=self.school)
        self.grade1 = Grade.objects.create(value=1,subject=self.subject,student=self.student)
        self.grade2 = Grade.objects.create(value=1)
    def test_school_str_method(self):
        self.assertEquals(str(self.school), 'School1')
    
    def test_post_str_method(self):
        self.assertEquals(str(self.post), 'Post1')

    def test_student_str_method(self):
        self.assertEquals(str(self.student), 'Student' + ' ' + 'StudentLast')

    def test_school_class_str_method(self):
        self.assertEquals(str(self.school_class), '1')
    
    def test_subject_str_method(self):
        self.assertEquals(str(self.subject), 'subject')
    
    def test_teacher_str_method(self):
        self.assertEquals(str(self.teacher), 'John' + ' ' + 'Smith')
    
    def test_principal_str_method(self):
        self.assertEquals(str(self.principal), 'Principal' + ' ' + 'PrincipalLast')

    def test_grade_full_str_method(self):
        self.assertEquals(str(self.grade1), str(self.grade1.value) + ' for ' +  str(self.grade1.student) + ' ' + str(self.grade1.subject.name) + ':' + str(self.subject.teacher))
    
    def test_grade_only_value_str_method(self):
        self.assertEquals(str(self.grade2), 'null')
    
    

    

