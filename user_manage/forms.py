# forms.py

from django import forms
from user_manage.models import Student,Teacher

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('username','password','nick_name',
                  'phone_number','wechat_id','wechat_name')

class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('username','password',
                  'phone_number','is_admin')

class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('username','password',
                  'phone_number')

