from django import forms
from django.contrib.auth.models import User
from .models import Profile

# تحديث بيانات المستخدم
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# تحديث صورة البروفايل
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
