from identify.models import Person
from django import forms


class UserForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['firstName', 'lastName', 'code', 'facePicture']
