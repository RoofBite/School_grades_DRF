from rest_framework import permissions
from .models import PrincipalTeacher, School, SchoolClass, SchoolSubject, Student, Teacher, User, Post


class SchoolPostDetailAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id

class SchoolPostsTeacherOrPrincipalPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_superuser:
            return True
        pk = request.resolver_match.kwargs.get('pk')
        
        if Teacher.objects.filter(user__id=request.user.id).exists():
            
            teacher_school_ids = Teacher.objects.get(user__id=request.user.id).school.values_list('id', flat = True)     
        else:
            teacher_school_ids = None
        
        if PrincipalTeacher.objects.filter(user__id=request.user.id).exists():
            principal_school_id = PrincipalTeacher.objects.get(user__id=request.user.id).school_id
        else:
            principal_school_id = None
        
        if teacher_school_ids:
            return pk in teacher_school_ids
        
        if principal_school_id == pk:
            return True
        
        return False



class SubjectTeacherPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_superuser:
            return True
        pk = request.resolver_match.kwargs.get('pk')
        if Teacher.objects.filter(user__id=request.user.id, schoolsubject__id=pk).exists():
            return True
        else:
            return False

class StudentGradePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method =='GET':
            pk2 = request.resolver_match.kwargs.get('pk2')
            return pk2 == request.user.id

class SubjectTeacherGradePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        pk1 = request.resolver_match.kwargs.get('pk1')
        pk2 = request.resolver_match.kwargs.get('pk2')
        
        if Student.objects.filter(subject__id=pk1, user__id=pk2, subject__teacher__user__id=request.user.id).exists():
            return True
        else:
            return False
            

class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_superuser:
            return True
        # Checks if id of school on that route is in id's of schools to which the teacher is asigned 
        user = User.objects.filter(id = request.user.id).first()
        pk = request.resolver_match.kwargs.get('pk')
        obj = Student.objects.filter(school__id = pk)
        teacher_school_id = False

        try:
            if user.teacher:
                # Obtains list of id's of schools to which teacher is assigned
                teacher_school_id = user.teacher.school.all().values_list('id', flat = True)
            else:
                teacher_school_id = False
        except:
            print("User is not teacher")

        # Attempts to take id of school to which student is assigned
        if not obj.first():
            student_school_id = False
        else:
            student_school_id = obj.first().school.id

        # Grants permission if student and teacher are asigned to the same school
        if student_school_id == False or teacher_school_id == False:
            return False
        else:
            return student_school_id in teacher_school_id
        
class PrincipalPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_superuser:
            return True

        # Checks if id of school on that route is in id's of schools to which the principal is asigned 
        user = User.objects.filter(id = request.user.id).first()
        pk = request.resolver_match.kwargs.get('pk')
        obj = Student.objects.filter(school__id = pk)
        principal_school_id = False

        try:
            if user.principalteacher:
                principal_school_id = user.principalteacher.school.id
            else:
                principal_school_id = False
        except:
            print("User is not principal")

        if not obj.first():
            student_school_id = False
        else:
            student_school_id = obj.first().school.id

        if student_school_id == False or principal_school_id == False:
            return False
        else:
            return student_school_id == principal_school_id