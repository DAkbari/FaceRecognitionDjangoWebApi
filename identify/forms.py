from identify.models import Person
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django import forms


class UserForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['firstName', 'lastName', 'code', 'facePicture']
        labels = {'firstName': 'نام',
                  'lastName': 'نام خانوادگی',
                  'code': 'کد پرسنلی',
                  'facePicture': 'تصویر'}


class ImageForm(forms.ModelForm):
    attached_photo = forms.FileField()


class NewUser(forms.Form):
    first_name = forms.CharField(max_length=100, label='نام', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            # 'placeholder': 'نام کاربری'
        }
    ))
    last_name = forms.CharField(max_length=100, label='نام خانوادگی', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    username = forms.CharField(max_length=100, label='نام کاربری', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    password = forms.CharField(max_length=100, label='گذرواژه', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    passwordConformation = forms.CharField(max_length=100, label='تکرار گذرواژه', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    email = forms.CharField(max_length=100, label='ایمیل', widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
        }
    ))
    captcha = CaptchaField(label='تشخیص هویت')





