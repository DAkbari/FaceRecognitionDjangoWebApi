from django.db import models
from django.urls import reverse


class Person(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    faceEncode = models.FileField()
    facePicture = models.FileField()
    lastLoginPicture = models.FileField()
    code = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('identify:detail', kwargs={'pk': self.pk})


