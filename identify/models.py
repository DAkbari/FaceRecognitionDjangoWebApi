from django.db import models
from django.urls import reverse



class Person(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    faceEncode = models.FileField(upload_to="encodes/")
    facePicture = models.FileField(upload_to="faces/")
    lastLoginPicture = models.FileField(upload_to='lastPhoto/')
    code = models.CharField(max_length=100)

    def as_json(self):
        return dict(firsName=self.firstName,
                    lastName=self.lastName,
                    code=self.code)

    def get_absolute_url(self):
        return reverse('identify:detail', kwargs={'pk': self.pk})


