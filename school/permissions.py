from rest_framework import permissions
from .models import School, SchoolClass, SchoolSubject, Student, Teacher, User


class SubjectTeacherPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_staff:
            return True
        pk = request.resolver_match.kwargs.get('pk')

        try:
            if Teacher.objects.get(user__id=request.user.id, schoolsubject__id=pk):
                return True
            else:
                return False
        except:
            print("User is not subject teacher")

class StudentGradesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print('permision request.user.id', request.user.id)
        if request.method=='GET':
            pk2 = request.resolver_match.kwargs.get('pk2')
            print(pk2)
            return pk2== request.user.id

class SubjectTeacherGradesPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('permision SubjectTeacherGradesPermission')
        return obj.subject__teacher__user__id == request.user.id
    


class TeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # If user is Admin permission is granted 
        if request.user.is_staff:
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
        if request.user.is_staff:
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